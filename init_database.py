from app import create_app, db
from flask_migrate import Migrate, upgrade

def init_db():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Run migrations
        upgrade()

if __name__ == '__main__':
    init_db() 