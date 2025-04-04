from database.db import db
from datetime import datetime, timezone

class Job(db.Model):
    """Model for job listings."""
    __tablename__ = 'job'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    candidates = db.relationship('Candidate', backref='job', lazy=True, cascade='all, delete-orphan')
    shortlisted_candidates = db.relationship('ShortlistedCandidate', 
                                          backref=db.backref('job_listing', lazy=True),
                                          lazy=True, 
                                          cascade='all, delete-orphan')

    def get_candidate_count(self):
        """Get the total number of candidates for this job."""
        return len(self.candidates)

    def get_shortlisted_count(self):
        """Get the number of shortlisted candidates for this job."""
        return len(self.shortlisted_candidates) 