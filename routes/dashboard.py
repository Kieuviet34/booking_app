from flask import Blueprint, render_template, session, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

mysql = MySQL()

def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    wrap.__name__ = f.__name__
    return wrap

@dashboard_bp.route('/dashboard')
@admin_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM patients WHERE is_deleted = 0")
    total_patients = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM staff WHERE is_deleted = 0")
    total_staff = cur.fetchone()[0]

    cur.execute("SELECT SUM(amount) FROM finances WHERE type = 'income'")
    total_income = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(amount) FROM finances WHERE type = 'expense'")
    total_expense = cur.fetchone()[0] or 0

    today = datetime.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = start_of_month.replace(month=start_of_month.month % 12 + 1, day=1)
    end_of_month = next_month - timedelta(seconds=1)
    cur.execute("""
        SELECT DAY(transaction_date), SUM(amount) 
        FROM finances 
        WHERE type = 'income' AND transaction_date BETWEEN %s AND %s 
        GROUP BY DAY(transaction_date)
    """, (start_of_month, end_of_month))
    revenue_data = cur.fetchall()

    days_in_month = end_of_month.day
    labels = [f"Ngày {day}" for day in range(1, days_in_month + 1)]
    data = [0] * days_in_month
    for day, amount in revenue_data:
        data[day - 1] = float(amount) if amount else 0

    cur.close()
    return render_template('dashboard.html', 
                           total_patients=total_patients,
                           total_appointments=total_appointments,
                           total_staff=total_staff,
                           total_income=total_income,
                           total_expense=total_expense,
                           labels=labels,
                           data=data)