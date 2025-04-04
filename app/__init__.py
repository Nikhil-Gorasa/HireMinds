from flask import Flask
from database.db import db
from flask_migrate import Migrate
import os

def create_app():
    app = Flask(__name__)
    
    # Configure the database
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recruitment.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app

# This file makes the app directory a Python package 