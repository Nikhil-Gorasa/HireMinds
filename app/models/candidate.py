from database.db import db
from datetime import datetime, timezone

class Candidate(db.Model):
    """Model for job candidates."""
    __tablename__ = 'candidate'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cv_text = db.Column(db.Text, nullable=False)
    analysis = db.Column(db.Text)  # Store the analysis as JSON string
    match_score = db.Column(db.Float, default=0.0)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applied_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    shortlisted = db.Column(db.Boolean, default=False)
    shortlisted_at = db.Column(db.DateTime)

    def to_dict(self):
        """Convert candidate to dictionary format."""
        return {
            'id': self.id,
            'name': self.name,
            'cv_text': self.cv_text,
            'analysis': self.analysis,
            'match_score': self.match_score,
            'job_id': self.job_id,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'shortlisted': self.shortlisted,
            'shortlisted_at': self.shortlisted_at.isoformat() if self.shortlisted_at else None
        } 