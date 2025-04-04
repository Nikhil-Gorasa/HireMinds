from database.db import db, Candidate, ShortlistedCandidate
from datetime import datetime, timedelta

def shortlist_candidates(job_id, threshold=0.8):
    """Shortlist candidates based on match score threshold."""
    try:
        # Get all candidates for the job with match score >= threshold
        candidates = Candidate.query.filter_by(job_id=job_id).filter(
            Candidate.match_score >= threshold
        ).all()

        # Create shortlisted entries
        for candidate in candidates:
            # Check if already shortlisted
            existing = ShortlistedCandidate.query.filter_by(
                candidate_id=candidate.id,
                job_id=job_id
            ).first()

            if not existing:
                shortlisted = ShortlistedCandidate(
                    candidate_id=candidate.id,
                    job_id=job_id,
                    interview_date=datetime.utcnow() + timedelta(days=7),  # Schedule 1 week from now
                    status='scheduled'
                )
                db.session.add(shortlisted)
                candidate.status = 'shortlisted'

        db.session.commit()
        return candidates
    except Exception as e:
        print(f"Error in shortlisting: {str(e)}")
        db.session.rollback()
        return []

def get_shortlisted_candidates(job_id):
    """Get all shortlisted candidates for a job."""
    try:
        return ShortlistedCandidate.query.filter_by(job_id=job_id).all()
    except Exception as e:
        print(f"Error getting shortlisted candidates: {str(e)}")
        return [] 