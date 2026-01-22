# Endpoints de administración: crear, listar y ver por id
# (Tema 2: Bluepoints y API REST, exige el enunciado separar dominios con Bluepoints
# Tema 3b: CRUD con SQLAlchemy y Flask, para operaciones CRUD
# Tema 3c: Autorización por roles JWT)
from flask import jsonify, request
from . import admin_bp
from app.models import Paciente, Doctor, Center
from app.utils.security import auth_required
from app.extensions import db

@admin_bp.get("/ping")
def ping():
    return jsonify({"ok": True, "service": "odonto_admin", "module": admin}), 200

#Crear paciente POST 
@admin_bp.post("/pacientes")
@auth_required(roles=["admin"])
def crear_paciente():
    data = request.get_json(force=True) or {}
    name = data.get("name")
    active = data.get("active", True)

    if not name:
        return jsonify({"ok": False, "error": {"code": "BAD_REQUEST", "message": "Name is required"}}), 400

    paciente = Paciente(name=name, active=active)
    db.session.add(paciente)
    db.session.commit()

    return jsonify({"ok": True, "data": {"id": paciente.id, "name": paciente.name, "active": paciente.active}}), 201

#Paciente
#Listar paciente GET
@admin_bp.get("/pacientes")
@auth_required(roles=["admin"])
def listar_pacientes():
    pacientes = Paciente.query.all()
    data = [
        {"id": p.id, "name": p.name, "active": p.active}
        for p in pacientes
    ]
    return jsonify({"ok": True, "data": data}), 200

#Ver paciente por ID GET
@admin_bp.get("/pacientes/<int:paciente_id>")
@auth_required(roles=["admin"])
def obtener_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)
    if not paciente:
        return jsonify({"ok": False, "error": {"code": "NOT_FOUND", "message": "Paciente no encontrado"}}), 404

    return jsonify({"ok": True, "data": {"id": paciente.id, "name": paciente.name, "active": paciente.active}}), 200

#Actualizar paciente PUT
@admin_bp.put("/pacientes/<int:paciente_id>")
@auth_required(roles=["admin"])
def actualizar_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)
    if not paciente:
        return jsonify({"ok": False,"error": {"code": "NOT_FOUND", "message": "Paciente no encontrado"}}), 404

    data = request.get_json(force=True) or {}
    if "name" in data:
        paciente.name = data["name"]
    if "active" in data:
        paciente.active = data["active"]

    db.session.commit()

    return jsonify({"ok": True,"data": {"id": paciente.id, "name": paciente.name, "active": paciente.active}}), 200

#Borrar Paciente DELETE
@admin_bp.delete("/pacientes/<int:paciente_id>")
@auth_required(roles=["admin"])
def borrar_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)
    if not paciente:
        return jsonify({"ok": False,"error": {"code": "NOT_FOUND", "message": "Paciente no encontrado"}}), 404

    db.session.delete(paciente)
    db.session.commit()

    return jsonify({"ok": True, "message": "Paciente eliminado"}), 200

#Doctor
#Crear doctor - POST
@admin_bp.post("/doctors")
@auth_required(roles=["admin"])
def create_doctor():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    specialty = data.get("specialty")
    active = data.get("active", True)

    if not name:
        return jsonify({"ok": False,"error": {"code": "BAD_REQUEST", "message": "Name is required"}}), 400

    doctor = Doctor(name=name, specialty=specialty, active=active)
    db.session.add(doctor)
    db.session.commit()

    return jsonify({"ok": True,"data": {"id": doctor.id,"name": doctor.name,"specialty": doctor.specialty,"active": doctor.active}}), 201

# Listar doctores - GET
@admin_bp.get("/doctors")
@auth_required(roles=["admin"])
def list_doctors():
    doctors = Doctor.query.all()
    data = [{"id": d.id, "name": d.name, "specialty": d.specialty, "active": d.active}
        for d in doctors
    ]
    return jsonify({"ok": True, "data": data}), 200

#Obtener por ID GET
@admin_bp.get("/doctors/<int:doctor_id>")
@auth_required(roles=["admin"])
def get_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"ok": False,"error": {"code": "NOT_FOUND", "message": "Doctor not found"}}), 404

    return jsonify({"ok": True,"data": {"id": doctor.id,"name": doctor.name,"specialty": doctor.specialty,"active": doctor.active}}), 200

#Actualizar - PUT
@admin_bp.put("/doctors/<int:doctor_id>")
@auth_required(roles=["admin"])
def update_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"ok": False,"error": {"code": "NOT_FOUND", "message": "Doctor not found"}}), 404

    data = request.get_json(silent=True) or {}
    if "name" in data:
        doctor.name = data["name"]
    if "specialty" in data:
        doctor.specialty = data["specialty"]
    if "active" in data:
        doctor.active = data["active"]

    db.session.commit()

    return jsonify({"ok": True,"data": {"id": doctor.id,"name": doctor.name,"specialty": doctor.specialty,"active": doctor.active}}), 200

#Borrar DELETE
@admin_bp.delete("/doctors/<int:doctor_id>")
@auth_required(roles=["admin"])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"ok": False,"error": {"code": "NOT_FOUND", "message": "Doctor not found"}}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({"ok": True, "message": "Doctor deleted"}), 200

#Center
# Crear center - POST
@admin_bp.post("/centers")
@auth_required(roles=["admin"])
def create_center():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    address = data.get("address")
    active = data.get("active", True)

    if not name:
        return jsonify({"ok": False,"error": {"code": "BAD_REQUEST", "message": "Name is required"}}), 400

    center = Center(name=name, address=address, active=active)
    db.session.add(center)
    db.session.commit()

    return jsonify({"ok": True,"data": {"id": center.id,"name": center.name,"address": center.address,"active": center.active}}), 201

#Listar centre - GET
@admin_bp.get("/centers")
@auth_required(roles=["admin"])
def list_centers():
    centers = Center.query.all()
    data = [
        {"id": c.id, "name": c.name, "address": c.address, "active": c.active}
        for c in centers
    ]
    return jsonify({"ok": True, "data": data}), 200

#Obtener por ID - GET
@admin_bp.get("/centers/<int:center_id>")
@auth_required(roles=["admin"])
def get_center(center_id):
    center = Center.query.get(center_id)
    if not center:
        return jsonify({"ok": False,"error": {"code": "NOT_FOUND", "message": "Center not found"}}), 404

    return jsonify({"ok": True,"data": {"id": center.id,"name": center.name,"address": center.address,"active": center.active}}), 200

#Actualizar - PUT
@admin_bp.put("/centers/<int:center_id>")
@auth_required(roles=["admin"])
def update_center(center_id):
    center = Center.query.get(center_id)
    if not center:
        return jsonify({
            "ok": False,
            "error": {"code": "NOT_FOUND", "message": "Center not found"}
        }), 404

    data = request.get_json(silent=True) or {}
    if "name" in data:
        center.name = data["name"]
    if "address" in data:
        center.address = data["address"]
    if "active" in data:
        center.active = data["active"]

    db.session.commit()

    return jsonify({"ok": True,"data": {"id": center.id,"name": center.name,"address": center.address,"active": center.active}}), 200

#Borrar - DELETE
@admin_bp.delete("/centers/<int:center_id>")
@auth_required(roles=["admin"])
def delete_center(center_id):
    center = Center.query.get(center_id)
    if not center:
        return jsonify({"ok": False,"error": {"code": "NOT_FOUND", "message": "Center not found"}}), 404

    db.session.delete(center)
    db.session.commit()

    return jsonify({"ok": True, "message": "Center deleted"}), 200
