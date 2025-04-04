from database.db import db
from datetime import datetime, timezone
import re

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

    def get_shortlist_status(self):
        """Get the shortlist status of the candidate."""
        if hasattr(self, 'shortlisted_candidate') and self.shortlisted_candidate:
            return self.shortlisted_candidate.status
        return 'Pending'

    def extract_email(self):
        """Extract email from CV text using regex."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(email_pattern, self.cv_text)
        return matches[0] if matches else None

    def send_interview_invite(self, meeting_data):
        """Send interview invite email to candidate."""
        from flask_mail import Message
        from flask import current_app
        from app import mail
        
        email = self.extract_email()
        if not email:
            raise ValueError("No email found in CV")

        subject = f"Interview Invitation - {current_app.config['COMPANY_NAME']}"
        
        body = f"""Dear {self.name},

We are pleased to invite you for an interview for the position you applied for.

Interview Details:
Date & Time: {meeting_data['meetingDate']}
Duration: {meeting_data['meetingDuration']} minutes
Meeting Link: {meeting_data['meetingLink']}

{meeting_data.get('additionalNotes', '')}

Please confirm your attendance by clicking the meeting link at the scheduled time.

Best regards,
{current_app.config['COMPANY_NAME']} Recruitment Team
"""
        
        msg = Message(
            subject=subject,
            recipients=[email],
            body=body
        )
        
        mail.send(msg)
        return True 