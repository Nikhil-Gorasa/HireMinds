from database.db import db
from app.models.candidate import Candidate
from app.models.shortlisted_candidate import ShortlistedCandidate
from datetime import datetime, timezone

def shortlist_candidates(job_id, threshold=0.8):
    """Shortlist candidates for a job based on match score."""
    # Get candidates with match score >= threshold
    candidates = Candidate.query.filter(
        Candidate.job_id == job_id,
        Candidate.match_score >= threshold
    ).all()
    
    count = 0
    for candidate in candidates:
        # Check if already shortlisted
        if not ShortlistedCandidate.query.filter_by(
            candidate_id=candidate.id,
            job_id=job_id
        ).first():
            # Create new shortlisted candidate
            shortlisted = ShortlistedCandidate(
                candidate_id=candidate.id,
                job_id=job_id,
                shortlisted_at=datetime.now(timezone.utc)
            )
            db.session.add(shortlisted)
            count += 1
    
    db.session.commit()
    return count

def get_shortlisted_candidates(job_id):
    """Get all shortlisted candidates for a job."""
    return ShortlistedCandidate.query.filter_by(job_id=job_id).all() 