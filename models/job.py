from database.db import db
from datetime import datetime

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    candidates = db.relationship('Candidate', backref='job', lazy=True)
    shortlisted_candidates = db.relationship('ShortlistedCandidate', backref='job', lazy=True)

    def __repr__(self):
        return f'<Job {self.title}>' 