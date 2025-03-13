from app import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))  # Có thể NULL nếu chỉ có 1 bác sĩ
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='new')
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('appointments', lazy=True))

    def __repr__(self):
        return f"<Appointment {self.id} - {self.status}>"
