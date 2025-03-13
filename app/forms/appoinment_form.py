from flask_wtf import FlaskForm
from wtforms import IntegerField, DateTimeField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

class AppointmentForm(FlaskForm):
    patient_id = IntegerField('ID Bệnh nhân', validators=[DataRequired()])
    staff_id = IntegerField('ID Nhân viên', validators=[DataRequired()])
    start_time = DateTimeField('Thời gian bắt đầu', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    end_time = DateTimeField('Thời gian kết thúc', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    status = StringField('Trạng thái', validators=[DataRequired()])
    note = TextAreaField('Ghi chú')
    submit = SubmitField('Lưu')
