import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app():

    app = Flask(__name__, instance_relative_config=False)
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    db.init_app(app)

    with app.app_context():

        from .home import home
        from .search_page import search_page

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(search_page.search_page_bp)

        return app
