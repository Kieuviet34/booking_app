from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    # TODO: Quản lý toàn bộ hệ thống, người dùng...
    return render_template('admin/dashboard.html')
