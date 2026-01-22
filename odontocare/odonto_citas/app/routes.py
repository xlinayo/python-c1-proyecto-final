# Se definen los endpoints REST del microservicio
# Contiene la API pública. Se crean las citas, se consultan las citas y se valida la disponibilidad
# (Tema 2: API REST, Tema 3c: Reglas de negocio y Tema 4 Comunicación entre microservicios)

from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import requests

from .models import Appointment
from .extensions import db

# En local funciona con localhost; en Docker se inyecta:
# ADMIN_BASE_URL=http://odonto_admin:5001
ADMIN_BASE_URL = os.getenv("ADMIN_BASE_URL", "http://localhost:5001")

citas_bp = Blueprint("citas_bp", __name__)

@citas_bp.post("/appointments")
def create_appointment():
    data = request.get_json(silent=True) or {}

    doctor_id = data.get("doctor_id")
    center_id = data.get("center_id")
    patient_name = data.get("patient_name")
    appointment_time = data.get("appointment_time")

    if not all([doctor_id, center_id, patient_name, appointment_time]):
        return jsonify({
            "ok": False,
            "error": {"code": "BAD_REQUEST", "message": "Missing fields"}
        }), 400

    # Validar doctor y center contra odonto_admin
    admin_url = f"{ADMIN_BASE_URL}/admin"

    # Reenviar el token tal como venga (si viene)
    incoming_auth = request.headers.get("Authorization", "")
    headers = {}
    if incoming_auth:
        headers["Authorization"] = incoming_auth  # ya viene "Bearer <token>"

    doctor_resp = requests.get(f"{admin_url}/doctors/{doctor_id}", headers=headers, timeout=10)
    center_resp = requests.get(f"{admin_url}/centers/{center_id}", headers=headers, timeout=10)

    if doctor_resp.status_code != 200 or center_resp.status_code != 200:
        return jsonify({
            "ok": False,
            "error": {"code": "NOT_FOUND", "message": "Doctor or Center not found"}
        }), 404

    try:
        appointment_dt = datetime.fromisoformat(appointment_time)
    except ValueError:
        return jsonify({
            "ok": False,
            "error": {"code": "BAD_REQUEST", "message": "appointment_time must be ISO format"}
        }), 400

    conflict = Appointment.query.filter_by(
        doctor_id=doctor_id,
        appointment_time=appointment_dt
    ).first()

    if conflict:
        return jsonify({
            "ok": False,
            "error": {"code": "CONFLICT", "message": "Doctor not available at that time"}
        }), 409

    appt = Appointment(
        doctor_id=doctor_id,
        center_id=center_id,
        patient_name=patient_name,
        appointment_time=appointment_dt
    )

    db.session.add(appt)
    db.session.commit()

    return jsonify({
        "ok": True,
        "data": {
            "id": appt.id,
            "doctor_id": appt.doctor_id,
            "center_id": appt.center_id,
            "patient_name": appt.patient_name,
            "appointment_time": appt.appointment_time.isoformat()
        }
    }), 201
