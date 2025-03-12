from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: xử lý form đăng nhập
        # user = ...
        # if user and check_password_hash(user.password, form_password):
        #     session['user_id'] = user.id
        #     ...
        flash("Đăng nhập thành công!", "success")
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # TODO: xử lý form đăng ký
        # new_user = ...
        # db.session.add(new_user)
        # db.session.commit()
        flash("Đăng ký thành công!", "success")
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/register.html')
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Đăng xuất thành công.", "success")
    return redirect(url_for('auth.login'))
