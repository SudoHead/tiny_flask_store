import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Flask Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')
    TEMPLATES_FOLDER = 'templates'

    VERIFICATION_TIME=2592000
    CONFIRMATION_TIME=2592000


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI')
    print(SQLALCHEMY_DATABASE_URI, 'prod')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
    print(SQLALCHEMY_DATABASE_URI, 'dev')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False