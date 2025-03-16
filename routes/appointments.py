from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

mysql = MySQL()

def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    wrap.__name__ = f.__name__
    return wrap

@appointments_bp.route('/appointments')
@admin_required
def appointments():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM appointments")
    appointments = cur.fetchall()
    cur.close()
    return render_template('appointments.html', appointments=appointments)

@appointments_bp.route('/add_appointment', methods=['GET', 'POST'])
@admin_required
def add_appointment():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        staff_id = request.form['staff_id'] or None
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        status = request.form['status']
        note = request.form['note']
        symptoms = request.form['symptoms']
        cur.execute("""
            INSERT INTO appointments (patient_id, staff_id, start_time, end_time, status, note, symptoms)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (patient_id, staff_id, start_time, end_time, status, note, symptoms))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('appointments.appointments'))
    cur.execute("SELECT id, name FROM patients WHERE is_deleted = 0")
    patients = cur.fetchall()
    cur.execute("SELECT id, full_name FROM staff WHERE is_deleted = 0")
    staff_list = cur.fetchall()
    cur.close()
    return render_template('add_appointment.html', patients=patients, staff_list=staff_list)

@appointments_bp.route('/update_appointment/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_appointment(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        staff_id = request.form['staff_id'] or None
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        status = request.form['status']
        note = request.form['note']
        symptoms = request.form['symptoms']
        cur.execute("""
            UPDATE appointments 
            SET patient_id=%s, staff_id=%s, start_time=%s, end_time=%s, status=%s, note=%s, symptoms=%s 
            WHERE id=%s
        """, (patient_id, staff_id, start_time, end_time, status, note, symptoms, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('appointments.appointments'))
    else:
        cur.execute("SELECT * FROM appointments WHERE id=%s", (id,))
        appointment = cur.fetchone()
        cur.execute("SELECT id, name FROM patients WHERE is_deleted = 0")
        patients = cur.fetchall()
        cur.execute("SELECT id, full_name FROM staff WHERE is_deleted = 0")
        staff_list = cur.fetchall()
        cur.close()
        return render_template('update_appointment.html', appointment=appointment, 
                               patients=patients, staff_list=staff_list)

@appointments_bp.route('/delete_appointment/<int:id>')
@admin_required
def delete_appointment(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM appointments WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('appointments.appointments'))