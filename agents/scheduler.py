from database.db import db
from app.models.shortlisted_candidate import ShortlistedCandidate
from datetime import datetime, timezone, timedelta

def schedule_interviews(job_id):
    """Schedule interviews for shortlisted candidates."""
    # Get all shortlisted candidates without interview dates
    candidates = ShortlistedCandidate.query.filter_by(
        job_id=job_id,
        interview_date=None,
        status='pending'
    ).all()
    
    if not candidates:
        return 0
    
    # Start scheduling from tomorrow
    interview_date = datetime.now(timezone.utc).replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
    count = 0
    
    for candidate in candidates:
        # Schedule 1-hour interviews
        candidate.interview_date = interview_date
        candidate.status = 'scheduled'
        interview_date += timedelta(hours=1)
        count += 1
    
    db.session.commit()
    return count

def get_scheduled_interviews(job_id):
    """Get all scheduled interviews for a job."""
    return ShortlistedCandidate.query.filter_by(
        job_id=job_id,
        status='scheduled'
    ).order_by(ShortlistedCandidate.interview_date).all() 