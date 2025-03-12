from app import db
from sqlalchemy.orm import validates
import re

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.String(50), nullable=False)  # Có thể chuyển thành db.Date nếu cần
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Một bệnh nhân có thể có nhiều lịch hẹn
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    @validates('email')
    def validate_email(self, key, value):
        if value and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email address")
        return value

    @validates('age')
    def validate_age(self, key, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        if value > 120:
            raise ValueError("Age must not exceed 120")
        return value

    def __repr__(self):
        return f"<Patient {self.name}>"
