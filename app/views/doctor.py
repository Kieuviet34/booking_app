from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.doctor import Doctor
from app import db

doctor_bp = Blueprint('doctor', __name__, template_folder='../templates/doctor')

@doctor_bp.route('/dashboard')
def dashboard():
    doctor_id = session.get('user_id')
    if doctor_id:
        doctor_member = Doctor.query.get(doctor_id)
        appointments = doctor_member.appointments if doctor_member else []
    else:
        appointments = []
        flash("Vui lòng đăng nhập với tư cách nhân viên để truy cập dashboard.", "warning")
    return render_template('dashboard.html', appointments=appointments)

@doctor_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    doctor_id = session.get('user_id')
    if not doctor_id:
        flash("Vui lòng đăng nhập để truy cập hồ sơ.", "warning")
        return redirect(url_for('auth.login'))
    doctor_member = Doctor.query.get(doctor_id)
    if request.method == 'POST':
        doctor_member.name = request.form.get('name')
        doctor_member.email = request.form.get('email')
        doctor_member.contact_number = request.form.get('contact_number')
        # Cập nhật các trường khác nếu cần...
        db.session.commit()
        flash("Cập nhật hồ sơ thành công.", "success")
        return redirect(url_for('doctor.profile'))
    return render_template('profile.html', doctor=doctor_member)
