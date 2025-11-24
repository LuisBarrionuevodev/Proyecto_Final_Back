import os

from dotenv import load_dotenv

load_dotenv()


def _env(name, default=None):
    return os.getenv(name, default)


class DevConfig:
    SECRET_KEY = _env("SECRET_KEY", "default-dev-key")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = _env("DATABASE_URI")
