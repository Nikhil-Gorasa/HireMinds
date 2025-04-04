from flask import Flask
from database.db import db
from app.models.job import Job
from app.models.candidate import Candidate
from app.models.shortlisted_candidate import ShortlistedCandidate
import os

def init_db(app):
    """Initialize the database with all required tables."""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    app = Flask(__name__)
    
    # Configure the database
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'recruitment.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database
    db.init_app(app)
    init_db(app) 