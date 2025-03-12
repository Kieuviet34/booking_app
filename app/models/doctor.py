from app import db
from sqlalchemy.orm import validates
import re

class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specialisation = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)  # Có thể dùng db.Date hoặc db.DateTime
    end_date = db.Column(db.String(50))
    contact_number = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Một doctor có thể có nhiều lịch hẹn
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    @validates('email')
    def validate_email(self, key, value):
        if value and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValueError("Invalid email address")
        return value

    def __repr__(self):
        return f"<doctor {self.name}>"
