from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL

staff_bp = Blueprint('staff', __name__)

mysql = MySQL()

def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    wrap.__name__ = f.__name__
    return wrap

@staff_bp.route('/staff')
@admin_required
def staff():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, full_name, phone, email, address, status FROM staff WHERE is_deleted = 0")
    staff_list = cur.fetchall()
    cur.close()
    return render_template('staff.html', staff=staff_list)

@staff_bp.route('/add_staff', methods=['GET', 'POST'])
@admin_required
def add_staff():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        specialty_id = request.form.get('specialty_id', None)
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO staff (full_name, phone, email, address, specialty_id, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (full_name, phone, email, address, specialty_id, status))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('staff.staff'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM specialties")
    specialties = cur.fetchall()
    cur.close()
    return render_template('add_staff.html', specialties=specialties)

@staff_bp.route('/update_staff/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_staff(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        specialty_id = request.form.get('specialty_id', None)
        status = request.form['status']
        cur.execute("""
            UPDATE staff 
            SET full_name=%s, phone=%s, email=%s, address=%s, specialty_id=%s, status=%s
            WHERE id=%s
        """, (full_name, phone, email, address, specialty_id, status, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('staff.staff'))
    else:
        cur.execute("SELECT * FROM staff WHERE id=%s", (id,))
        staff_member = cur.fetchone()
        cur.execute("SELECT id, name FROM specialties")
        specialties = cur.fetchall()
        cur.close()
        return render_template('update_staff.html', staff=staff_member, specialties=specialties)

@staff_bp.route('/delete_staff/<int:id>')
@admin_required
def delete_staff(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE staff SET is_deleted=1 WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('staff.staff'))

@staff_bp.route('/search_staff', methods=['POST'])
@admin_required
def search_staff():
    data = request.get_json()
    query = data.get('query', '').strip()

    try:
        cur = mysql.connection.cursor()
        sql_query = """
            SELECT id, full_name, phone, email, address, status 
            FROM staff 
            WHERE is_deleted = 0 
            AND (full_name LIKE %s OR phone LIKE %s OR email LIKE %s)
        """
        search_term = f"%{query}%"
        cur.execute(sql_query, (search_term, search_term, search_term))
        staff_list = cur.fetchall()
        cur.close()
        return jsonify({'staff': staff_list})
    except mysql.connector.Error as err:
        return jsonify({'error': f'Lỗi cơ sở dữ liệu: {str(err)}'}), 500