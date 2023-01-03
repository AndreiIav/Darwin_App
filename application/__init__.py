from flask import Flask
from os import path
from pathlib import Path


def init_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile(path.join(Path.cwd(), "config.py"))

    with app.app_context():

        from . import db

        db.init_app(app)

        from . import routes

        return app
