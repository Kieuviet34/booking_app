from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL

finance_bp = Blueprint('finance', __name__)

mysql = MySQL()

def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    wrap.__name__ = f.__name__
    return wrap

@finance_bp.route('/finance')
@admin_required
def finance():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, transaction_date, amount, type, description, created_at, updated_at FROM finances")
    finances = cur.fetchall()
    cur.close()
    return render_template('finance.html', finances=finances)

@finance_bp.route('/add_finance', methods=['GET', 'POST'])
@admin_required
def add_finance():
    if request.method == 'POST':
        transaction_date = request.form['transaction_date']
        amount = request.form['amount']
        type_ = request.form['type']
        description = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO finances (transaction_date, amount, type, description)
            VALUES (%s, %s, %s, %s)
        """, (transaction_date, amount, type_, description))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('finance.finance'))
    return render_template('add_finance.html')

@finance_bp.route('/update_finance/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_finance(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        transaction_date = request.form['transaction_date']
        amount = request.form['amount']
        type_ = request.form['type']
        description = request.form['description']
        cur.execute("""
            UPDATE finances 
            SET transaction_date=%s, amount=%s, type=%s, description=%s
            WHERE id=%s
        """, (transaction_date, amount, type_, description, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('finance.finance'))
    cur.execute("SELECT id, transaction_date, amount, type, description, created_at, updated_at FROM finances WHERE id=%s", (id,))
    finance = cur.fetchone()
    cur.close()
    return render_template('update_finance.html', finance=finance)

@finance_bp.route('/delete_finance/<int:id>')
@admin_required
def delete_finance(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM finances WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('finance.finance'))

@finance_bp.route('/search_finance', methods=['POST'])
@admin_required
def search_finance():
    data = request.get_json()
    query = data.get('query', '').strip()

    try:
        cur = mysql.connection.cursor()
        sql_query = """
            SELECT id, transaction_date, amount, type, description, created_at, updated_at
            FROM finances 
            WHERE description LIKE %s OR type LIKE %s OR amount LIKE %s
        """
        search_term = f"%{query}%"
        cur.execute(sql_query, (search_term, search_term, search_term))
        finances = cur.fetchall()
        cur.close()
        return jsonify({'finances': [list(f) for f in finances]})
    except mysql.connector.Error as err:
        return jsonify({'error': f'Lỗi cơ sở dữ liệu: {str(err)}'}), 500

@finance_bp.route('/export_finance')
@admin_required
def export_finance():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, transaction_date, amount, type, description, created_at, updated_at FROM finances")
    finances = cur.fetchall()
    cur.close()
    return jsonify({'finances': [list(f) for f in finances]})