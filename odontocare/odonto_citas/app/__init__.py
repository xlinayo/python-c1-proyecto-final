# Crea y configura la aplicación Flask del microservicio citas
# Centraliza la creación de la app, registra los Blueprints y permite una arquitectura modular y escalable
# (Tema 2 API REST con Flask, Blueprints y organización del proyectos Flask
# Tema 3b SQLAlchemy y Flask gestión de contexto de aplicación)

from flask import Flask
from .routes import citas_bp
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///citas.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(citas_bp)

    with app.app_context():
        db.create_all()

    return app
