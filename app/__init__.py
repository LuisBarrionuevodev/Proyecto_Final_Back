from flask import Flask
from flask_migrate import Migrate

from app.config import get_config
from app.database import db

migrate = Migrate()


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(get_config())

    db.init_app(flask_app)
    from app import models

    migrate.init_app(flask_app, db)
    return flask_app
