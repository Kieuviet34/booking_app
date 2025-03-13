from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email(message="Email không hợp lệ")])
    phone = StringField('Số điện thoại', validators=[DataRequired(), Length(min=10, max=15)])
    address = StringField('Địa chỉ', validators=[DataRequired(), Length(min=5, max=100)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Xác nhận mật khẩu', validators=[
        DataRequired(), EqualTo('password', message='Mật khẩu không khớp')
    ])
    submit = SubmitField('Đăng ký')

class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Đăng nhập')
