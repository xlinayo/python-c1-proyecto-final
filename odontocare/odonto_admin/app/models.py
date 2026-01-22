# Crear modelo User. Los campos mínimos son: id, username, password_hash y role
# Se importa werkzeug.security
# (Tema 3b: Persistencia de datos con SQLAlchemy, creacion del modelo, creacion de tablas
# y CRUD)

from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#Definicion de modelos, tipos de columnas y valores por defecto (Tema 3b)
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password_hash = db.Column(db.String(225), nullable = False)
    role = db.Column(db.String(20), nullable = False, default = "admin")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
# Paciente
class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

#Doctor
class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), nullable=True)
    active = db.Column(db.Boolean, default=True)

#Center
class Center(db.Model):
    __tablename__ = "centers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=True)
