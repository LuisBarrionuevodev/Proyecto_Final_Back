# app/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (en la raíz del proyecto)
load_dotenv()


class BaseConfig:
    """Config base para todas las envs."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Si no hay var de entorno, caemos a SQLite local
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///dev.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
    DEBUG = False


class ProdConfig(BaseConfig):
    DEBUG = False


def get_config(config_name: str | None = None):
    """
    Devuelve la clase de configuración según FLASK_ENV o parámetro explícito.
    """
    env = (config_name or os.getenv("FLASK_ENV", "development")).lower()

    if env.startswith("prod"):
        return ProdConfig
    if env.startswith("test"):
        return TestConfig
    return DevConfig
