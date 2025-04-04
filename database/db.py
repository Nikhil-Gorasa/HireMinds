from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    candidates = db.relationship('Candidate', backref='job', lazy=True)
    shortlisted_candidates = db.relationship('ShortlistedCandidate', backref='job', lazy=True)

    def get_shortlisted_count(self):
        return len(self.shortlisted_candidates)

    def get_candidate_count(self):
        return len(self.candidates)

    def get_average_match_score(self):
        if not self.candidates:
            return 0.0
        return sum(c.match_score for c in self.candidates) / len(self.candidates)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cv_text = db.Column(db.Text, nullable=False)
    match_score = db.Column(db.Float)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shortlisted = db.relationship('ShortlistedCandidate', backref='candidate', lazy=True)

    def is_shortlisted(self):
        return len(self.shortlisted) > 0

    def get_interview_date(self):
        if self.shortlisted:
            return self.shortlisted[0].interview_date
        return None

class ShortlistedCandidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    interview_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_candidate_name(self):
        return self.candidate.name

    def get_job_title(self):
        return self.job.title 