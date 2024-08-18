import logging
import os
import sqlite3
from pathlib import Path

from concurrent_log_handler import ConcurrentTimedRotatingFileHandler
from flask import Flask, render_template
from flask.logging import default_handler
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# -------------
# Configuration
# -------------

db = SQLAlchemy()
csrf = CSRFProtect()
cache = Cache()

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
    register_error_pages(app)
    configure_logging(app)

    if config_type in ("config.DevelopmentConfig", "config.ProductionConfig"):
        run_warm_up_queries(app, "app.db")

    return app


# ----------------
# Helper Functions
# ----------------


def register_blueprints(app):
    # Import the blueprints
    from application.cli_database.cli import cli_database_bp
    from application.home.home_routes import home_bp
    from application.search_page.search_page_routes import search_page_bp

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(search_page_bp)
    app.register_blueprint(cli_database_bp)


def initialize_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)


def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template("405.html"), 405


def configure_logging(app):
    # Logging Configuration
    file_handler = ConcurrentTimedRotatingFileHandler(
        "instance/Darwin_App.log",
        when="D",
        interval=1,
        backupCount=20,
        maxBytes=1048576,  # 10 MB
        encoding="utf-8",
    )
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    # Log that the Flask application is starting
    app.logger.info("Starting the Flask Darwin_App...")


def run_warm_up_queries(app, database_name):
    with app.app_context():
        database_name = database_name
        database_folder = Path(app.config["DATABASE_FOLDER"])
        database_path = database_folder / database_name

        try:
            conn = sqlite3.connect(database_path)
            c = conn.cursor()

            with conn:
                c.execute(
                    """
                    SELECT m.id, m.name, my.id , my.magazine_id , my.year, mn.id,
                    mn.magazine_year_id, mn.magazine_number
                    FROM magazines m 
                    INNER JOIN magazine_year my ON m.id = my.magazine_id 
                    INNER JOIN magazine_number mn ON my.id = mn.magazine_year_id 
                    """
                )
                res = c.fetchall()
                app.logger.info(f"warm_up query 1 executed: {len(res)} rows returned")

                c.execute(
                    """
                    SELECT mnc.id, mnc.magazine_number_id, mnc.magazine_page,
                    mncf.rowid
                    FROM magazine_number_content mnc
                    INNER JOIN magazine_number_content_fts mncf
                    ON mnc.rowid = mncf.rowid
                    """
                )
                res = c.fetchall()
                app.logger.info(f"warm_up query 2 executed: {len(res)} rows returned")

        except sqlite3.Error as err:
            app.logger.error(
                "warm_up queries not executed in run_warm_up_queries() because"
                f" of sqlite3.Error: {err}"
            )
