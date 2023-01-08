from flask import Flask
from os import path
from pathlib import Path


def init_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile(path.join(Path.cwd(), "config.py"))

    with app.app_context():

        from . import db

        db.init_app(app)

        from .home import home
        from .search_page import search_page

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(search_page.search_page_bp)

        return app
