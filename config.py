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
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        default=b"\xe7\xc86\x9c\x0c\x9a\xcbiw3#)1\xd0\xde\x95\xb8\x8a[Q\xf9\xc4\x81\xf9\xdc\x84\x14Qu\xf6\xdeu",
    )

    # Pagination
    RESULTS_PER_PAGE = 10
    ERROR_OUT = True

    # Placeholder text for search bar
    PLACEHOLDER_TEXT_FOR_SEARCH_BAR = "you can enter between 4 and 200 characters"

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


class ProductionConfig(Config):
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TESTING_SQLALCHEMY_DATABASE_URI",
        default=f"sqlite:///{os.path.join(BASEDIR,'instance','test.db')}",
    )

    # Environment variables
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
