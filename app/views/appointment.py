from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.staff import Staff
from app import db
from datetime import datetime

appointment_bp = Blueprint('appointment_bp', __name__)

@appointment_bp.route('/dashboard')
def dashboard():
    appointments = Appointment.query.all()
    return render_template('appointment/dashboard.html', appointments=appointments)

@appointment_bp.route('/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        staff_id = request.form.get('staff_id')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        status = request.form.get('status')
        note = request.form.get('note')
        new_appt = Appointment(
            patient_id=patient_id,
            staff_id=staff_id,
            start_time=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S'),
            end_time=datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S'),
            status=status,
            note=note
        )
        db.session.add(new_appt)
        db.session.commit()
        flash("Lịch hẹn được tạo thành công", "success")
        return redirect(url_for('appointment_bp.dashboard'))
    patients = Patient.query.all()
    staffs = Staff.query.all()
    return render_template('appointment/add_appointment.html', patients=patients, staffs=staffs)

@appointment_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    appt = Appointment.query.get_or_404(id)
    if request.method == 'POST':
        appt.patient_id = request.form.get('patient_id')
        appt.staff_id = request.form.get('staff_id')
        appt.start_time = datetime.strptime(request.form.get('start_time'), '%Y-%m-%d %H:%M:%S')
        appt.end_time = datetime.strptime(request.form.get('end_time'), '%Y-%m-%d %H:%M:%S')
        appt.status = request.form.get('status')
        appt.note = request.form.get('note')
        db.session.commit()
        flash("Lịch hẹn đã được cập nhật", "success")
        return redirect(url_for('appointment_bp.dashboard'))
    patients = Patient.query.all()
    staffs = Staff.query.all()
    return render_template('appointment/edit_appointment.html', appt=appt, patients=patients, staffs=staffs)

@appointment_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appt = Appointment.query.get_or_404(id)
    db.session.delete(appt)
    db.session.commit()
    return '', 204
