from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


# -------------
# Configuration
# -------------

db = SQLAlchemy()

# ----------------------------
# Application Factory Function
# ----------------------------


def init_app():

    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)

    return app


# ----------------
# Helper Functions
# ----------------


def register_blueprints(app):
    # Import the blueprints
    from application.home.home import home_bp
    from application.search_page.search_page import search_page_bp

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(search_page_bp)


def initialize_extensions(app):
    db.init_app(app)
