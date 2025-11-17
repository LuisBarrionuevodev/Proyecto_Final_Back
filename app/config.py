import os

from dotenv import load_dotenv

load_dotenv()  # lee el .env


class BaseConfig:
    """Configuración base para la aplicación."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        # Formato recomendado para MySQL (usar variables reales en .env):
        # mysql+pymysql://usuario:password@localhost:3306/devvproyectofinal?charset=utf8mb4
        "sqlite:///dev.db",  # fallback si no hay .env
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    DEBUG = False


def get_config():
    """Devuelve la clase de configuración según FLASK_ENV."""

    env = os.getenv("FLASK_ENV", "development").lower()
    if env.startswith("prod"):
        return ProdConfig
    if env.startswith("test"):
        return TestConfig
    return DevConfig

