from database.db import db
from datetime import datetime, timezone

class ShortlistedCandidate(db.Model):
    """Model for shortlisted candidates."""
    __tablename__ = 'shortlisted_candidate'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    shortlisted_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    interview_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, scheduled, completed, cancelled
    
    # Relationships
    candidate = db.relationship('Candidate', backref=db.backref('shortlisted_candidate', uselist=False))
    
    def get_candidate_name(self):
        """Get the name of the shortlisted candidate."""
        return self.candidate.name if self.candidate else "Unknown" 