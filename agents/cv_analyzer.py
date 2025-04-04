import ollama
from database.db import db
from app.models.candidate import Candidate
from app.models.job import Job
from datetime import datetime, timezone
import json

def analyze_cv(cv_text, job_summary):
    """Analyze CV against job requirements and compute match score."""
    try:
        prompt = f"""Analyze this candidate's CV against the job requirements and provide a match score between 0 and 1.
        Consider the following aspects:
        1. Skills match
        2. Experience level
        3. Qualifications
        4. Overall fit
        
        Job Requirements:
        {job_summary}
        
        Candidate's CV:
        {cv_text}
        
        Return only a number between 0 and 1 representing the match score, where:
        - 1.0: Perfect match
        - 0.8-0.9: Strong match
        - 0.6-0.7: Moderate match
        - <0.6: Poor match"""
        
        response = ollama.chat(model='tinyllama:latest', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        # Extract the score from the response
        score_text = response['message']['content'].strip()
        try:
            score = float(score_text)
            return max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
        except ValueError:
            print(f"Error parsing score: {score_text}")
            return 0.0
            
    except Exception as e:
        print(f"Error in CV analysis: {str(e)}")
        return 0.0

def store_candidate(name, cv_text, job_id, analysis=None):
    """Store a candidate in the database."""
    candidate = Candidate(
        name=name,
        cv_text=cv_text,
        job_id=job_id,
        analysis=json.dumps(analysis) if analysis else None,
        match_score=analysis.get('match_score', 0.0) if analysis else 0.0
    )
    db.session.add(candidate)
    db.session.commit()
    return candidate 