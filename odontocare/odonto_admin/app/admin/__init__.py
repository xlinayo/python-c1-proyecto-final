# Se define el Blueprint de admin, ya que el módulo administrativo se debe configurar por separado
# (Tema 2: Bluepoints y API REST, exige el enunciado separar dominios con Bluepoints
# Tema 3b: CRUD con SQLAlchemy y Flask, para operaciones CRUD)
from flask import Blueprint

admin_bp = Blueprint("admin", __name__)