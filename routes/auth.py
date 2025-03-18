from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import bcrypt
from MySQLdb import IntegrityError, Error  # Import đúng các ngoại lệ từ MySQLdb

auth_bp = Blueprint('auth', __name__)

mysql = MySQL()

def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    wrap.__name__ = f.__name__
    return wrap

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT username, password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                session['logged_in'] = True
                session['username'] = username
                session['admin'] = True
                return jsonify({'success': True})
            else:
                return jsonify({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'})
        except Error as err:  # Sử dụng Error từ MySQLdb thay vì mysql.connector.Error
            return jsonify({'error': f'Lỗi cơ sở dữ liệu: {str(err)}'})
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        phone = data['phone']
        address = data['address']
        password = data['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            cur = mysql.connection.cursor()
            # Kiểm tra xem username hoặc email đã tồn tại chưa
            cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            if cur.fetchone():
                cur.close()
                return jsonify({'error': 'Tên đăng nhập hoặc email đã tồn tại'})
            cur.execute("""
                INSERT INTO users (username, password, phone, email, address, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (username, hashed_password.decode('utf-8'), phone, email, address, first_name, last_name))
            mysql.connection.commit()
            cur.close()
            return jsonify({'success': True})
        except IntegrityError as err:  # Bắt lỗi khi vi phạm ràng buộc UNIQUE
            return jsonify({'error': f'Lỗi cơ sở dữ liệu: Tên đăng nhập hoặc email đã tồn tại - {str(err)}'})
        except Error as err:  # Bắt các lỗi cơ sở dữ liệu khác
            return jsonify({'error': f'Lỗi cơ sở dữ liệu: {str(err)}'})
    return render_template('register.html')

@auth_bp.route('/forgot_password')
def forgot_password():
    return "Trang quên mật khẩu"

@auth_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('admin', None)
    return redirect(url_for('auth.login'))