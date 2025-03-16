from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

finance_bp = Blueprint('finance', __name__)

mysql = MySQL()
def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    wrap.__name__ = f.__name__
    return wrap
@finance_bp.route('/finance')
@admin_required
def finance():
    return render_template('finance.html')