from app import db

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    appointment_type = db.Column(db.String(255))
    appointment_date = db.Column(db.String(50), nullable=False)  
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Khóa ngoại liên kết với bảng patients và doctors
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))

    def __repr__(self):
        return f"<Appointment {self.id} - {self.appointment_type}>"
