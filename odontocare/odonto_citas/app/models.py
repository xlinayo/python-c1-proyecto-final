# Se define el modelo de datos Appointment
# Las citas persisten en la base de datos y se mantiene la independencia del microservicio admin
# (Tema 3b: Persistencia con SQLAlchemy)
from app.extensions import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, nullable=False)
    center_id = db.Column(db.Integer, nullable=False)
    patient_name = db.Column(db.String(120), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
