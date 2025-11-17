from flask import Flask
from flask_migrate import Migrate

from .config import get_config
from .database import db

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
    from .routes import actuaciones_bp, health_bp  # noqa: WPS433

    app.register_blueprint(health_bp, url_prefix="/api/v1/health")
    app.register_blueprint(actuaciones_bp, url_prefix="/api/v1/actuaciones")

    @app.get("/")
    def root():
        return {"message": "Bromatologia API"}, 200

    return app
