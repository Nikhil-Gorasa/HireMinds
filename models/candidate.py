from database.db import db
from datetime import datetime

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cv_text = db.Column(db.Text, nullable=False)
    match_score = db.Column(db.Float, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shortlisted = db.relationship('ShortlistedCandidate', backref='candidate', uselist=False)

    def __repr__(self):
        return f'<Candidate {self.name}>' 