"""Flask configuration"""

from dotenv import load_dotenv
import os


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

    # Preview string
    PREVIEW_SUBSTRING_LENGTH = 200

    ROOT_FOLDER = BASEDIR


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
    SERVER_NAME = "localhost.localdomain:5000"
