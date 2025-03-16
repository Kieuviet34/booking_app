from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL

patients_bp = Blueprint('patients', __name__)

mysql = MySQL()

def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    wrap.__name__ = f.__name__
    return wrap

@patients_bp.route('/patients')
@admin_required
def patients():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, phone, email, address, note FROM patients WHERE is_deleted = 0")
    patients = cur.fetchall()
    cur.close()
    return render_template('patients.html', patients=patients)

@patients_bp.route('/add_patient', methods=['GET', 'POST'])
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
        return redirect(url_for('patients.patients'))
    return render_template('add_patient.html')

@patients_bp.route('/update_patient/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('patients.patients'))
    else:
        cur.execute("SELECT * FROM patients WHERE id=%s", (id,))
        patient = cur.fetchone()
        cur.close()
        return render_template('update_patient.html', patient=patient)

@patients_bp.route('/delete_patient/<int:id>')
@admin_required
def delete_patient(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE patients SET is_deleted=1 WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('patients.patients'))

@patients_bp.route('/search_patients', methods=['POST'])
@admin_required
def search_patients():
    data = request.get_json()
    query = data.get('query', '').strip()

    try:
        cur = mysql.connection.cursor()
        sql_query = """
            SELECT id, name, phone, email, address, note 
            FROM patients 
            WHERE is_deleted = 0 
            AND (name LIKE %s OR phone LIKE %s OR email LIKE %s)
        """
        search_term = f"%{query}%"
        cur.execute(sql_query, (search_term, search_term, search_term))
        patients = cur.fetchall()
        cur.close()
        return jsonify({'patients': patients})
    except mysql.connector.Error as err:
        return jsonify({'error': f'Lỗi cơ sở dữ liệu: {str(err)}'}), 500