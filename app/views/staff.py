from flask import Blueprint, render_template
from app.models.staff import Staff
from app import db
staff_bp = Blueprint('staff_bp', __name__)

@staff_bp.route('/dashboard')
def dashboard():
    staffs = Staff.query.all()
    return render_template('staff/dashboard.html', staffs=staffs)
@staff_bp.route('/add', methods=['GET', 'POST'])
def add_staff():
    pass
@staff_bp.route('edit/<int:id>', methods=['GET', 'POST'])
def edit_staff(id):
    pass
@staff_bp.route('delete/<int:id>', methods=['DELETE'])
def delete_staff(id):
    staff = Staff.query.get_or_404(id)
    db.session.delete(staff)
    db.session.commit()
    return '', 204