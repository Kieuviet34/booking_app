from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class PatientForm(FlaskForm):
    name = StringField('Tên bệnh nhân', validators=[DataRequired(), Length(min=3, max=255)])
    phone = StringField('Số điện thoại', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Địa chỉ', validators=[DataRequired(), Length(min=5, max=255)])
    note = TextAreaField('Ghi chú', validators=[Length(max=500)])
    submit = SubmitField('Lưu')
