"""Flask configuration"""

import os

from dotenv import load_dotenv

# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Specificy a `.env` file containing key/value config values and load values from it
load_dotenv(os.path.join(BASEDIR, ".env"))


class Config(object):
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEVELOPMENT_SQLALCHEMY_DATABASE_URI",
        default=f"sqlite:///{os.path.join(BASEDIR, 'instance','app.db')}",
    )
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Environment variables
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False

    # Pagination
    RESULTS_PER_PAGE = 10
    ERROR_OUT = True

    # Placeholder text for search bar
    PLACEHOLDER_TEXT_FOR_SEARCH_BAR = "you can enter between 4 and 200 characters"

    # SQLITE FTS5 additional non alphanumeric unicode characters considered
    # token characters
    ACCEPTED_FTS5_SPECIAL_CHARACTERS = "-_.,„!?;:''"

    # Preview string
    PREVIEW_SUBSTRING_LENGTH = 200

    # cli_database blueprint
    ROOT_FOLDER = BASEDIR
    DATABASE_FOLDER = os.path.join(ROOT_FOLDER, "instance")
    DATABASE_FILES = os.path.join(
        ROOT_FOLDER, "application", "cli_database", "create_database_files"
    )
    FILES_TO_TABLES = [
        ("magazines.csv", "magazines"),
        ("magazine_years.csv", "magazine_year"),
        ("magazine_numbers.csv", "magazine_number"),
        ("magazine_content.csv", "magazine_number_content"),
    ]

    # Flask-Caching SimpleCache backend
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

    # Logging
    LOG_WITH_GUNICORN = os.getenv("LOG_WITH_GUNICORN", default=False)


class ProductionConfig(Config):
    FLASK_ENV = "production"
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Flask-Caching Redis backend
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    CACHE_REDIS_DB = 0
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = "darwin_app_cache_"


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "development_secret_key"


class TestingConfig(Config):
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TESTING_SQLALCHEMY_DATABASE_URI",
        default=f"sqlite:///{os.path.join(BASEDIR,'instance','test.db')}",
    )

    # Environment variables
    SECRET_KEY = "test_secret_key"
    TESTING = True

    # cli_database blueprint test
    FILES_TO_TABLES = [
        ("magazines_test_data.csv", "magazines"),
        ("magazine_year_test_data.csv", "magazine_year"),
        ("magazine_number_test_data.csv", "magazine_number"),
        ("magazine_number_content_test_data.csv", "magazine_number_content"),
    ]
    DATABASE_FILES = os.path.join(BASEDIR, "tests", "test_data")

    # WTF_CSFR
    WTF_CSRF_ENABLED = False


class DemoConfig(Config):
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEMO_SQLALCHEMY_DATABASE_URI",
        default=f"sqlite:///{os.path.join(BASEDIR,'instance','demo.db')}",
    )

    SECRET_KEY = "demo_secret_key"
