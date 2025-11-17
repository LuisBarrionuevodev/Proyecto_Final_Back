# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # lee el .env

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
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
    env = os.getenv("FLASK_ENV", "development").lower()
    if env.startswith("prod"):
        return ProdConfig
    if env.startswith("test"):
        return TestConfig
    return DevConfig

