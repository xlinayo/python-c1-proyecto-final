# Se crea la app Flask, carga config, inicializa extensiones y registra Blueprints
# Arquitectura modulas para que el servicio sea escalable y fácil de probar
# (Tema 2: REST API con Flask, Blueprints (organización modular))
from flask import Flask, jsonify
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Blueprints
    from .auth import auth_bp
    from .admin import admin_bp

    #Importar routes para registrar los endpoints
    from .auth import routes as _auth_routes
    from .admin import routes as _admin_routes

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Global
    @app.get("/ping")
    def ping():
        return jsonify({"ok": True, "service": "odonto_admin"}), 200
    
    # Errores en JSON
    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"ok": False, "error": {"code": "NOT_FOUND", "message": "Route not found"}}), 404
    
    #Importar users
    from app.models import User

    # Crear la tabla de users. Importar User, buscar si existe admin y si no existe l ocrea, para eso es admin123
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username = "admin").first()
        if not admin:
            admin = User(username = "admin", role = "admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

    return app


