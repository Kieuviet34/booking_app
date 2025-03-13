from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.finance import Finance
from app import db
from datetime import datetime

finance_bp = Blueprint('finance_bp', __name__)

@finance_bp.route('/dashboard')
def dashboard():
    finances = Finance.query.all()
    return render_template('finance/dashboard.html', finances=finances)

@finance_bp.route('/add', methods=['GET', 'POST'])
def add_finance():
    if request.method == 'POST':
        transaction_date = request.form.get('transaction_date')
        amount = request.form.get('amount')
        type_ = request.form.get('type')
        description = request.form.get('description')
        new_finance = Finance(
            transaction_date=datetime.strptime(transaction_date, '%Y-%m-%d'),
            amount=amount,
            type=type_,
            description=description
        )
        db.session.add(new_finance)
        db.session.commit()
        flash("Giao dịch thu chi được thêm thành công", "success")
        return redirect(url_for('finance_bp.dashboard'))
    return render_template('finance/add_finance.html')

@finance_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_finance(id):
    finance = Finance.query.get_or_404(id)
    db.session.delete(finance)
    db.session.commit()
    return '', 204
