# app/__init__.py
import os

from flask import Flask
from flask_cors import CORS  # 👈 NUEVO
from flask_migrate import Migrate

from .config import get_config
from .database import db

migrate = Migrate()


def create_app() -> Flask:
    """
    App factory principal.

    - Carga config desde .env (via get_config).
    - Inicializa SQLAlchemy y Flask-Migrate.
    - Registra los blueprints.
    """
    app = Flask(__name__)

    # 1) Cargar la clase de config (sin parámetros, como la tenés ahora)
    cfg = get_config()
    app.config.from_object(cfg)

    # 2) Safety net: si por algún motivo todavía no hay URI, la seteamos
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        uri = os.getenv("SQLALCHEMY_DATABASE_URI")
        if not uri:
            uri = "sqlite:///dev.db"
        app.config["SQLALCHEMY_DATABASE_URI"] = uri

    # 3) Inicializar extensiones principales
    db.init_app(app)
    migrate.init_app(app, db)

    # 4) Habilitar CORS para las rutas /api/*
    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:5173"}},
        supports_credentials=False,
    )

    # 5) Registrar blueprints
    from .routes import actuaciones_bp, health_bp  # noqa: WPS433

    app.register_blueprint(health_bp, url_prefix="/api/v1/health")
    app.register_blueprint(actuaciones_bp, url_prefix="/api/v1/actuaciones")

    # 6) Ruta raíz de prueba
    @app.get("/")
    def root():
        return {"message": "Bromatologia API"}, 200

    return app
