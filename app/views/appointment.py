from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.appointment import Appointment
from app import db

appointment_bp = Blueprint('appointment', __name__, template_folder='../templates/appointment')

@appointment_bp.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        appointment_type = request.form.get('appointment_type')
        appointment_date = request.form.get('appointment_date')
        # Lấy patient_id từ session, giả sử chỉ bệnh nhân mới đặt lịch
        patient_id = session.get('user_id')
        # Lấy doctor_id từ form hoặc xác định theo logic nghiệp vụ
        doctor_id = request.form.get('doctor_id')
        if not patient_id:
            flash("Bạn cần đăng nhập với tư cách bệnh nhân để đặt lịch.", "warning")
            return redirect(url_for('auth.login'))  
        new_appointment = Appointment(
            appointment_type=appointment_type,
            appointment_date=appointment_date,
            patient_id=patient_id,
            doctor_id=doctor_id
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash("Đặt lịch khám thành công!", "success")
        return redirect(url_for('appointment.list_appointments'))
    return render_template('book.html')

@appointment_bp.route('/list')
def list_appointments():
    # Lấy danh sách lịch hẹn; có thể lọc theo người dùng dựa trên session hoặc hiển thị tất cả cho admin
    appointments = Appointment.query.all()
    return render_template('list.html', appointments=appointments)
