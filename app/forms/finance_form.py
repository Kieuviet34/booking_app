from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class FinanceForm(FlaskForm):
    transaction_date = DateField('Ngày giao dịch', format='%Y-%m-%d', validators=[DataRequired()])
    amount = DecimalField('Số tiền', validators=[DataRequired()])
    type = StringField('Loại giao dịch', validators=[DataRequired()])  # hoặc sử dụng SelectField cho 'income'/'expense'
    description = StringField('Mô tả')
    submit = SubmitField('Lưu')
