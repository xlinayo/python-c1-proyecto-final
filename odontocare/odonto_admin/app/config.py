# Se realiza una configuración centralizada y separada del código donde 
# se pueden usar variables de entorno, clave para Docker (Tema 2: configuración de
# Flask y Tema 4: Docker)

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///admin.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False