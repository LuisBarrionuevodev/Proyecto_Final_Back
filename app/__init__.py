from flask import Flask
from flask_migrate import Migrate

from .database import db

migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    # 👉 CONFIG DIRECTA DE LA BASE (MySQL)
    # Cambiá "usuario", "password" y "devvproyectofinal" por los tuyos reales
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+mysqlclient://usuario:password@localhost:3306/devvproyectofinal?charset=utf8mb4"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret"

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
