from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'ThoSanTreEmX2004'  # Thay bằng key bảo mật của bạn

# Cấu hình MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kieuviet2004@'
app.config['MYSQL_DB'] = 'booking_app'

mysql = MySQL(app)

# Decorator kiểm tra quyền admin
def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrap.__name__ = f.__name__
    return wrap

# =============================
# 1. Đăng nhập, đăng xuất
# =============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Ví dụ cứng: username = "admin" và password = "12345"
        if username == 'admin' and password == '12345':
            session['admin'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Tên đăng nhập hoặc mật khẩu không đúng')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'admin' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# =============================
# 2. Dashboard
# =============================
@app.route('/dashboard')
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

# =============================
# 3. Quản lý bệnh nhân
# =============================
@app.route('/patients')
@admin_required
def patients():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients WHERE is_deleted = 0")
    patients = cur.fetchall()
    cur.close()
    return render_template('patients.html', patients=patients)

@app.route('/add_patient', methods=['GET', 'POST'])
@admin_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        note = request.form['note']
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO patients (name, phone, email, address, note) 
            VALUES (%s, %s, %s, %s, %s)
        """, (name, phone, email, address, note))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

@app.route('/update_patient/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_patient(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        note = request.form['note']
        cur.execute("""
            UPDATE patients 
            SET name=%s, phone=%s, email=%s, address=%s, note=%s 
            WHERE id=%s
        """, (name, phone, email, address, note, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('patients'))
    else:
        cur.execute("SELECT * FROM patients WHERE id=%s", (id,))
        patient = cur.fetchone()
        cur.close()
        return render_template('update_patient.html', patient=patient)

@app.route('/delete_patient/<int:id>')
@admin_required
def delete_patient(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE patients SET is_deleted=1 WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('patients'))

# =============================
# 4. Quản lý nhân viên (staff)
# =============================
@app.route('/staff')
@admin_required
def staff():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE is_deleted = 0")
    staff_list = cur.fetchall()
    cur.close()
    return render_template('staff.html', staff=staff_list)

@app.route('/add_staff', methods=['GET', 'POST'])
@admin_required
def add_staff():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        role = request.form['role']
        specialty = request.form.get('specialty', None)
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO staff (full_name, phone, email, address, role, specialty, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (full_name, phone, email, address, role, specialty, status))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('staff'))
    return render_template('add_staff.html')

@app.route('/update_staff/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_staff(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        role = request.form['role']
        specialty = request.form.get('specialty', None)
        status = request.form['status']
        cur.execute("""
            UPDATE staff 
            SET full_name=%s, phone=%s, email=%s, address=%s, role=%s, specialty=%s, status=%s
            WHERE id=%s
        """, (full_name, phone, email, address, role, specialty, status, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('staff'))
    else:
        cur.execute("SELECT * FROM staff WHERE id=%s", (id,))
        staff_member = cur.fetchone()
        cur.close()
        return render_template('update_staff.html', staff=staff_member)

@app.route('/delete_staff/<int:id>')
@admin_required
def delete_staff(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE staff SET is_deleted=1 WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('staff'))

# =============================
# 5. Quản lý lịch hẹn
# =============================
@app.route('/appointments')
@admin_required
def appointments():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM appointments")
    appointments = cur.fetchall()
    cur.close()
    return render_template('appointments.html', appointments=appointments)

@app.route('/add_appointment', methods=['GET', 'POST'])
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
        cur.execute("""
            INSERT INTO appointments (patient_id, staff_id, start_time, end_time, status, note)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (patient_id, staff_id, start_time, end_time, status, note))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('appointments'))
    cur.execute("SELECT id, name FROM patients WHERE is_deleted = 0")
    patients = cur.fetchall()
    cur.execute("SELECT id, full_name FROM staff WHERE is_deleted = 0")
    staff_list = cur.fetchall()
    cur.close()
    return render_template('add_appointment.html', patients=patients, staff_list=staff_list)

@app.route('/update_appointment/<int:id>', methods=['GET', 'POST'])
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
        cur.execute("""
            UPDATE appointments 
            SET patient_id=%s, staff_id=%s, start_time=%s, end_time=%s, status=%s, note=%s 
            WHERE id=%s
        """, (patient_id, staff_id, start_time, end_time, status, note, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('appointments'))
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

@app.route('/delete_appointment/<int:id>')
@admin_required
def delete_appointment(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM appointments WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('appointments'))

# =============================
# 6. Các filter cho template
# =============================
@app.template_filter('datetime_vn_day')
def datetime_vn_day(value):
    """
    Hiển thị 'Thứ x, dd/mm'. Ví dụ: 'Thứ 2, 15/3'
    """
    date_obj = datetime.strptime(value, '%Y-%m-%d')
    days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
    return f"{days[date_obj.weekday()]}, {date_obj.day}/{date_obj.month}"

@app.template_filter('datetime_vn')
def datetime_vn(value):
    """
    Hiển thị 'Thứ x, dd/mm/yyyy'
    """
    date_obj = datetime.strptime(value, '%Y-%m-%d')
    days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
    return f"{days[date_obj.weekday()]}, {date_obj.day}/{date_obj.month}/{date_obj.year}"

@app.template_filter('datetime_local')
def datetime_local(value):
    """
    Định dạng cho <input type='datetime-local'>
    """
    return value.strftime('%Y-%m-%dT%H:%M')

@app.template_filter('datetime_combine')
def datetime_combine(date_str, hour, minute=0):
    """
    Ghép date_str (YYYY-MM-DD) + hour + minute thành datetime.
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.replace(hour=hour, minute=minute, second=0, microsecond=0)

# =============================
# 7. Route Xếp lịch theo chuyên khoa
# =============================
@app.route('/schedule', methods=['GET', 'POST'])
@admin_required
def schedule():
    cur = mysql.connection.cursor()
    
    # Danh sách trạng thái để lọc
    statuses = ['new', 'confirmed', 'waiting', 'in_progress', 'done', 'cancelled']
    
    # Lấy trạng thái từ query (mặc định 'all')
    selected_status = request.args.get('status', 'all')
    status_filter = ""
    if selected_status != 'all':
        status_filter = f"AND a.status = '{selected_status}'"
    
    # Lấy ngày bắt đầu (mặc định ngày hiện tại)
    selected_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')
    
    # Lấy chuyên khoa từ query, mặc định "Khoa Khám bệnh đa khoa"
    selected_department = request.args.get('department', "Khoa Khám bệnh đa khoa")
    
    # Tạo danh sách 7 ngày của tuần để hiển thị với thông tin is_open theo chuyên khoa
    days_of_week = []
    for i in range(7):
        day_dt = selected_datetime + timedelta(days=i)
        weekday = day_dt.weekday()  # Monday=0, ..., Sunday=6
        is_open = True
        if selected_department == "Khoa Khám bệnh đa khoa":
            # Mở từ Thứ 2 (0) đến Thứ 6 (4)
            if weekday not in [0, 1, 2, 3, 4]:
                is_open = False
        elif selected_department == "Khoa Khám theo yêu cầu":
            # Mở từ Thứ 2 (0) đến Thứ 7 (5); Chủ nhật (6) đóng
            if weekday == 6:
                is_open = False
        elif selected_department == "Trung tâm khám sức khỏe định kỳ":
            # Mở từ Thứ 2 đến Thứ 7 (0-5); Chủ nhật (6) không khám
            if weekday == 6:
                is_open = False
        days_of_week.append({
            'date': day_dt.strftime('%Y-%m-%d'),
            'display': day_dt.strftime('%a, %d/%m'),
            'weekday': weekday,
            'is_open': is_open
        })
    
    # Xác định khoảng thời gian để lấy lịch hẹn: từ ngày bắt đầu đến ngày kết thúc của tuần
    start_of_week = selected_datetime
    end_of_week = selected_datetime + timedelta(days=6)
    
    # Lấy các lịch hẹn trong khoảng thời gian này, sử dụng "a.note as appointment_title"
    cur.execute(f"""
        SELECT a.id, a.note as appointment_title, p.name, a.staff_id, s.full_name, 
               a.start_time, a.end_time, a.status, a.symptoms
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        LEFT JOIN staff s ON a.staff_id = s.id
        WHERE a.start_time BETWEEN %s AND %s {status_filter}
    """, (start_of_week, end_of_week))
    appointments = cur.fetchall()
    
    # Lấy danh sách bác sĩ (role='doctor' và status='active')
    cur.execute("SELECT id, full_name, specialty FROM staff WHERE role='doctor' AND status='active'")
    doctors = cur.fetchall()
    
    # Lấy danh sách bệnh nhân
    cur.execute("SELECT id, name FROM patients WHERE is_deleted=0")
    patients = cur.fetchall()
    
    # Lấy doctor_id từ query (nếu có) để tính số ca làm việc, gợi ý, vv.
    doctor_id = request.args.get('doctor_id', None)
    doctor_workload = 0
    suggested_patients = []
    if doctor_id:
        cur.execute("""
            SELECT COUNT(*) FROM appointments 
            WHERE staff_id = %s AND start_time BETWEEN %s AND %s
        """, (doctor_id, start_of_week, end_of_week))
        doctor_workload = cur.fetchone()[0]
        # (Có thể thêm logic gợi ý bệnh nhân nếu cần)
    
    # Xử lý form POST để tạo mới lịch hẹn (xếp lịch thủ công)
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        appointment_title = request.form['appointment_name']  # Sử dụng note để lưu tên lịch hẹn
        symptoms = request.form.get('symptoms', '')
        doctor_id_form = request.form['doctor_id']
        patient_id_form = request.form['patient_id']
        start_time_form = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        end_time_form   = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
        
        # Kiểm tra xung đột lịch của bác sĩ (so sánh với work_schedules và appointments)
        cur.execute("""
            SELECT COUNT(*) FROM work_schedules
            WHERE staff_id = %s
              AND ((start_time <= %s AND end_time >= %s) OR (start_time <= %s AND end_time >= %s))
        """, (doctor_id_form, start_time_form, start_time_form, end_time_form, end_time_form))
        work_conflict = cur.fetchone()[0]
        
        cur.execute("""
            SELECT COUNT(*) FROM appointments
            WHERE staff_id = %s
              AND ((start_time <= %s AND end_time >= %s) OR (start_time <= %s AND end_time >= %s))
        """, (doctor_id_form, start_time_form, start_time_form, end_time_form, end_time_form))
        appointment_conflict = cur.fetchone()[0]
        
        if work_conflict == 0 and appointment_conflict == 0:
            # Insert lịch hẹn mới; lưu tên lịch hẹn vào cột note, status = 'confirmed'
            cur.execute("""
                INSERT INTO appointments (note, patient_id, staff_id, start_time, end_time, status, symptoms)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (appointment_title, patient_id_form, doctor_id_form, start_time_form, end_time_form, 'confirmed', symptoms))
            mysql.connection.commit()
        else:
            cur.close()
            return render_template('schedule.html',
                                   error="Bác sĩ không trống trong khung giờ này",
                                   appointments=appointments,
                                   doctors=doctors,
                                   patients=patients,
                                   selected_date=selected_date,
                                   statuses=statuses,
                                   selected_status=selected_status,
                                   doctor_id=doctor_id,
                                   doctor_workload=doctor_workload,
                                   suggested_patients=suggested_patients,
                                   days_of_week=days_of_week,
                                   selected_department=selected_department)
    
    cur.close()
    return render_template('schedule.html',
                           appointments=appointments,
                           doctors=doctors,
                           patients=patients,
                           selected_date=selected_date,
                           statuses=statuses,
                           selected_status=selected_status,
                           doctor_id=doctor_id,
                           doctor_workload=doctor_workload,
                           suggested_patients=suggested_patients,
                           days_of_week=days_of_week,
                           selected_department=selected_department)

# =============================
# Chạy ứng dụng
# =============================
if __name__ == '__main__':
    app.run(debug=True)
