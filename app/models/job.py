from database.db import db
from datetime import datetime, timezone

class Job(db.Model):
    """Model for job listings."""
    __tablename__ = 'job'
    
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column('title', db.String(200), nullable=False)
    _description = db.Column('description', db.Text, nullable=False)
    _requirements = db.Column('requirements', db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    candidates = db.relationship('Candidate', backref='job', lazy=True, cascade='all, delete-orphan')
    shortlisted_candidates = db.relationship('ShortlistedCandidate', 
                                          backref=db.backref('job_listing', lazy=True),
                                          lazy=True, 
                                          cascade='all, delete-orphan')

    @property
    def title(self):
        """Get cleaned title text."""
        return self._title.replace("'''", "").replace("''", "'").replace("'", "'") if self._title else ""

    @title.setter
    def title(self, value):
        """Set title with cleaning."""
        self._title = value.replace("'''", "").replace("''", "'").replace("'", "'") if value else ""

    @property
    def description(self):
        """Get cleaned description text."""
        return self._description.replace("'''", "").replace("''", "'").replace("'", "'") if self._description else ""

    @description.setter
    def description(self, value):
        """Set description with cleaning."""
        self._description = value.replace("'''", "").replace("''", "'").replace("'", "'") if value else ""

    @property
    def requirements(self):
        """Get cleaned requirements text."""
        return self._requirements.replace("'''", "").replace("''", "'").replace("'", "'") if self._requirements else ""

    @requirements.setter
    def requirements(self, value):
        """Set requirements with cleaning."""
        self._requirements = value.replace("'''", "").replace("''", "'").replace("'", "'") if value else ""

    def get_candidate_count(self):
        """Get the total number of candidates for this job."""
        return len(self.candidates)

    def get_shortlisted_count(self):
        """Get the number of shortlisted candidates for this job."""
        return len(self.shortlisted_candidates) 