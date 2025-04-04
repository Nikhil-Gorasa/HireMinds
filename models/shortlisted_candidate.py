from database.db import db
from datetime import datetime

class ShortlistedCandidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    interview_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_candidate_name(self):
        return self.candidate.name if self.candidate else "Unknown"

    def __repr__(self):
        return f'<ShortlistedCandidate {self.get_candidate_name()}>' 