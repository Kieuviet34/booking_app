from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta

schedule_bp = Blueprint('schedule', __name__)

mysql = MySQL()

def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    wrap.__name__ = f.__name__
    return wrap

def update_appointment_status():
    cur = mysql.connection.cursor()
    current_time = datetime.now()

    cur.execute("""
        SELECT a.id, ec.price
        FROM appointments a
        JOIN examination_categories ec ON a.examination_category_id = ec.id
        WHERE a.end_time < %s AND a.status != 'done'
    """, (current_time,))
    appointments_to_update = cur.fetchall()

    for appointment in appointments_to_update:
        appointment_id = appointment[0]
        price = appointment[1]
        cur.execute("""
            UPDATE appointments
            SET status = 'done'
            WHERE id = %s
        """, (appointment_id,))

        cur.execute("""
            INSERT INTO finances (transaction_date, amount, type, description)
            VALUES (%s, %s, 'income', %s)
        """, (current_time, price, f"Thu nhập từ lịch hẹn ID {appointment_id}"))
        mysql.connection.commit()
    cur.close()

@schedule_bp.route('/schedule', methods=['GET', 'POST'])
@admin_required
def schedule():
    update_appointment_status()
    cur = mysql.connection.cursor()
    statuses = ['new', 'confirmed', 'waiting', 'in_progress', 'done', 'cancelled']
    selected_status = request.args.get('status', 'all')
    status_filter = "" if selected_status == 'all' else f"AND a.status = '{selected_status}'"

    selected_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')

    cur.execute("SELECT id, name FROM specialty_categories")
    specialty_categories = cur.fetchall()
    selected_category_id = request.args.get('category_id', specialty_categories[0][0] if specialty_categories else None)

    if selected_category_id:
        cur.execute("SELECT id, name FROM specialties WHERE category_id = %s", (selected_category_id,))
        specialties = cur.fetchall()
    else:
        specialties = []
    selected_specialty_id = request.args.get('specialty_id', specialties[0][0] if specialties else None)
    doctors = []
    if selected_specialty_id:
        cur.execute("""
            SELECT staff.id, staff.full_name, specialties.name as specialty
            FROM staff
            LEFT JOIN specialties ON staff.specialty_id = specialties.id
            WHERE staff.role = 'doctor' AND staff.status = 'active' AND specialties.id = %s
        """, (selected_specialty_id,))
        doctors = cur.fetchall()

    doctor_id = request.args.get('doctor_id', None)

    days_of_week = []
    for i in range(7):
        day_dt = selected_datetime + timedelta(days=i)
        weekday = day_dt.weekday()
        is_open = weekday in [0, 1, 2, 3, 4, 5]
        days_of_week.append({
            'date': day_dt.strftime('%Y-%m-%d'),
            'display': day_dt.strftime('%a, %d/%m'),
            'weekday': weekday,
            'is_open': is_open
        })

    start_of_week = selected_datetime
    end_of_week = selected_datetime + timedelta(days=6)

    doctor_filter = " AND a.staff_id = %s" if doctor_id else ""
    params = [start_of_week, end_of_week]
    if doctor_id:
        params.append(doctor_id)

    query = f"""
        SELECT a.id, a.note as appointment_title, p.name, a.staff_id, s.full_name, 
               a.start_time, a.end_time, a.status, a.symptoms, ec.name as examination_category
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        LEFT JOIN staff s ON a.staff_id = s.id
        LEFT JOIN examination_categories ec ON a.examination_category_id = ec.id
        WHERE a.start_time BETWEEN %s AND %s {status_filter} {doctor_filter}
    """
    cur.execute(query, tuple(params))
    appointments = cur.fetchall()

    cur.execute("SELECT id, name, note, symptom FROM patients WHERE is_deleted=0")
    patients = cur.fetchall()

    cur.execute("SELECT id, name, price FROM examination_categories")
    examination_categories = cur.fetchall()

    current_time_str = datetime.now().strftime('%Y-%m-%dT%H:%M')

    if request.method == 'POST':
        appointment_title = request.form['appointment_name']
        symptoms = request.form.get('symptoms', '')
        doctor_id_form = request.form['doctor_id']
        patient_id_form = request.form['patient_id']
        examination_category_id = request.form['examination_category_id']
        start_time_form = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        end_time_form = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')

        current_time = datetime.now()
        start_hour = start_time_form.hour
        end_hour = end_time_form.hour

        if start_time_form < current_time:
            error = "Không thể đặt lịch cho thời gian đã qua."
        elif start_hour < 6 or start_hour >= 18 or end_hour < 6 or end_hour > 18:
            error = "Thời gian đặt lịch phải từ 6:00 AM đến 6:00 PM."
        else:
            cur.execute("""
                SELECT COUNT(*) FROM appointments
                WHERE staff_id = %s
                  AND ((start_time <= %s AND end_time >= %s) OR (start_time <= %s AND end_time >= %s))
            """, (doctor_id_form, start_time_form, start_time_form, end_time_form, end_time_form))
            appointment_conflict = cur.fetchone()[0]

            if appointment_conflict == 0:
                cur.execute("""
                    INSERT INTO appointments (note, patient_id, staff_id, start_time, end_time, status, symptoms, examination_category_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (appointment_title, patient_id_form, doctor_id_form, start_time_form, end_time_form, 'confirmed', symptoms, examination_category_id))
                mysql.connection.commit()
            else:
                error = "Bác sĩ không trống trong khung giờ này."

        if 'error' in locals():
            return render_template('schedule.html',
                                   error=error,
                                   specialty_categories=specialty_categories,
                                   selected_category_id=selected_category_id,
                                   specialties=specialties,
                                   selected_specialty_id=selected_specialty_id,
                                   doctors=doctors,
                                   patients=patients,
                                   examination_categories=examination_categories,
                                   selected_date=selected_date,
                                   statuses=statuses,
                                   selected_status=selected_status,
                                   doctor_id=doctor_id,
                                   days_of_week=days_of_week,
                                   appointments=appointments,
                                   current_time_str=current_time_str) 

    cur.close()
    return render_template('schedule.html',
                           specialty_categories=specialty_categories,
                           selected_category_id=selected_category_id,
                           specialties=specialties,
                           selected_specialty_id=selected_specialty_id,
                           doctors=doctors,
                           patients=patients,
                           examination_categories=examination_categories,
                           selected_date=selected_date,
                           statuses=statuses,
                           selected_status=selected_status,
                           doctor_id=doctor_id,
                           days_of_week=days_of_week,
                           appointments=appointments,
                           current_time_str=current_time_str) 