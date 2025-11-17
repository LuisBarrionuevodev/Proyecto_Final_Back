from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import get_config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str | None = None) -> Flask:
    """
    App factory principal.

    - Carga la config correcta (dev / test / prod).
    - Inicializa extensiones (db, migrate).
    - Registra el blueprint de la API (Flask-RESTX).
    """
    app = Flask(__name__)
    cfg = get_config(config_name)
    app.config.from_object(cfg)

    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar API REST
    from .api import api_bp  # noqa: WPS433 (import interno a propósito)

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.get("/")
    def root():
        return {"message": "Bromatologia API"}, 200

    return app
