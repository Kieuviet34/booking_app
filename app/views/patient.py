from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.patient import Patient
from app import db

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/dashboard')
def dashboard():
    patients = Patient.query.all()
    return render_template('patient/dashboard.html', patients=patients)

@patient_bp.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        note = request.form.get('note')
        new_patient = Patient(name=name, phone=phone, email=email, address=address, note=note)
        db.session.add(new_patient)
        db.session.commit()
        flash("Bệnh nhân được thêm thành công", "success")
        return redirect(url_for('patient_bp.dashboard'))
    return render_template('patient/add_patient.html')

@patient_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.phone = request.form.get('phone')
        patient.email = request.form.get('email')
        patient.address = request.form.get('address')
        patient.note = request.form.get('note')
        db.session.commit()
        flash("Thông tin bệnh nhân đã được cập nhật", "success")
        return redirect(url_for('patient_bp.dashboard'))
    return render_template('patient/edit_patient.html', patient=patient)

@patient_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return '', 204
