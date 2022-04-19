import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config, ProdConfig, DevConfig

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

def create_app():
    """Initialize the app"""
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    db.init_app(app)
    # initialize_db()
    
    # Register blueprints
    from . import store
    app.register_blueprint(store.store_bp)
    
    return app