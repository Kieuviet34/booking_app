from flask import Flask, session, redirect, url_for, render_template
from flask_mysqldb import MySQL
import bcrypt
from datetime import datetime
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.patients import patients_bp
from routes.staff import staff_bp
from routes.appointments import appointments_bp
from routes.schedule import schedule_bp
from routes.finance import finance_bp

app = Flask(__name__)
app.secret_key = 'ThoSanTreEmX2004'

# Cấu hình MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kieuviet2004@'
app.config['MYSQL_DB'] = 'booking_app'
mysql = MySQL(app)

# Đăng ký các Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(finance_bp)

# Filter cho template
@app.template_filter('strftime')
def strftime_filter(dt, fmt='%Y-%m-%dT%H:%M'):
    if isinstance(dt, datetime):
        return dt.strftime(fmt)
    return dt

@app.template_filter('datetime_vn_day')
def datetime_vn_day(value):
    date_obj = datetime.strptime(value, '%Y-%m-%d')
    days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
    return f"{days[date_obj.weekday()]}, {date_obj.day}/{date_obj.month}"

@app.template_filter('datetime_vn')
def datetime_vn(value):
    date_obj = datetime.strptime(value, '%Y-%m-%d')
    days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
    return f"{days[date_obj.weekday()]}, {date_obj.day}/{date_obj.month}/{date_obj.year}"

@app.template_filter('datetime_local')
def datetime_local_filter(value):
    return value.strftime('%Y-%m-%dT%H:%M')

@app.template_filter('datetime_combine')
def datetime_combine_filter(date_str, hour, minute=0):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.replace(hour=hour, minute=minute, second=0, microsecond=0)

# Route index
@app.route('/')
def index():
    if 'admin' in session:
        return redirect(url_for('dashboard.dashboard'))
    else:
        return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)