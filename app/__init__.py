from flask import Flask
from flask_migrate import Migrate

from .config import get_config
from .database import db

migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    # Configuración de la aplicación (carga desde .env mediante get_config)
    config_class = get_config()
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar y registrar blueprints
    from .routes import actuaciones_bp, health_bp  # noqa: WPS433

    app.register_blueprint(health_bp, url_prefix="/api/v1/health")
    app.register_blueprint(actuaciones_bp, url_prefix="/api/v1/actuaciones")

    @app.get("/")
    def root():
        return {"message": "Bromatologia API"}, 200

    return app
