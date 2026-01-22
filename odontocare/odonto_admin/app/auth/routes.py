# Endpoints de autenticación y se relacionan con tokens. El sistema tiene acceso controlado
# (Tema 2: API Rest con Flask, Tema 4: Seguridad con tokens, Respuestas JSON)
from flask import jsonify, request
from . import auth_bp
from app.models import User
from app.utils.security import create_token

@auth_bp.get("/ping")
def ping():
    return jsonify({"ok": True, "service": "odonto_admin", "module": "auth"}), 200

# Endpoint de login
@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"ok": False, "error": {"code": "BAD_REQUEST", "message": "username y password son obligatorios"}}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"ok": False, "error": {"code": "UNAUTHORIZED", "message": "Credenciales incorrectas"}}), 401

    token = create_token(user)
    return jsonify({"ok": True,"token": token,"username": user.username,"role": user.role}), 200


