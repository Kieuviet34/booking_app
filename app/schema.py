from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.patient import Patient
from app.models.staff import Doctor
from app.models.appointment import Appointment
from app.models.user import User

class PatientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        include_relationships = True
        load_instance = True

class StaffSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Doctor
        include_relationships = True
        load_instance = True

class AppointmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        include_relationships = True
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
