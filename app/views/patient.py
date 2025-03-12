from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.patient import Patient
from app import db

patient_bp = Blueprint('patient', __name__, template_folder='../templates/patient')

@patient_bp.route('/dashboard')
def dashboard():
    # Lấy thông tin bệnh nhân dựa trên session (user_id)
    patient_id = session.get('user_id')
    if patient_id:
        patient = Patient.query.get(patient_id)
        appointments = patient.appointments if patient else []
    else:
        appointments = []
        flash("Vui lòng đăng nhập với tư cách bệnh nhân để truy cập dashboard.", "warning")
    return render_template('dashboard.html', appointments=appointments)

@patient_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    patient_id = session.get('user_id')
    if not patient_id:
        flash("Vui lòng đăng nhập để truy cập hồ sơ.", "warning")
        return redirect(url_for('auth.login'))
    patient = Patient.query.get(patient_id)
    if request.method == 'POST':
        # Cập nhật thông tin bệnh nhân
        patient.name = request.form.get('name')
        patient.email = request.form.get('email')
        patient.contact_number = request.form.get('contact_number')
        # Cập nhật các trường khác nếu cần...
        db.session.commit()
        flash("Cập nhật hồ sơ thành công.", "success")
        return redirect(url_for('patient.profile'))
    return render_template('profile.html', patient=patient)
