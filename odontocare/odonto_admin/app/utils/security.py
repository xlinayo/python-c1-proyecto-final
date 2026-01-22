# Se genera utils para tener todos los archivos ordenados y no mezclar conceptos,
# ya que los archivos que conforman utils son transversales
# En este archivo security.py se desarrollan JWT y decoradores reutilizables
# con el objetivo de crear y validar tokens
# (auth_requires, validación de tokens y roles)
# (Tema 3c: autenticación básica de tokens y autorización)

import os
import jwt
from datetime import datetime, timedelta
from flask import current_app
from functools import wraps
from flask import request, jsonify, g

def _secret() -> str:
    # Usa SECRET_KEY de config.py
    return current_app.config["SECRET_KEY"]

def create_token(user, minutes: int = 60) -> str:
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes = minutes),
        "iat": datetime.utcnow()
    }
    # Algortimo de firma y verificacion HS256
    return jwt.encode(payload, _secret(), algorithm = "HS256")

def decode_token(token: str) -> dict:
    return jwt.decode(token, _secret(), algorithms = ["HS256"])

def auth_required(roles=None):
    roles = set(roles) if roles else None

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return jsonify({"ok": False, "error": {"code": "UNAUTHORIZED", "message": "Token Bearer missing"}}), 401
            
            token = auth.split(" ", 1)[1].strip()
            try:
                payload = decode_token(token)
            except Exception:
                return jsonify({"ok": False, "error": {"code": "UNAUTHORIZED", "message": "Invalid token"}}), 401
            
            if roles and payload.get("role") not in roles:
                return jsonify({"ok": False, "error": {"code": "FORBIDDEN", "message": "No permisos"}}), 403
            
            g.user = payload
            return fn(*args, **kwargs)
        return wrapper
    return decorator
