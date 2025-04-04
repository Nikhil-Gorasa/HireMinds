import ollama
from database.db import db
from app.models.candidate import Candidate
from app.models.job import Job
from datetime import datetime, timezone
import json

def analyze_cv(cv_text, job_summary):
    """Analyze CV against job requirements and compute match score."""
    try:
        prompt = f"""Analyze this candidate's CV against the job requirements and provide a detailed analysis in JSON format.
        
        Job Requirements:
        {job_summary}
        
        Candidate's CV:
        {cv_text}
        
        Provide your analysis in the following JSON format:
        {{
            "match_score": <float between 0 and 1>,
            "strengths": [<list of key strengths found in CV>],
            "weaknesses": [<list of areas where CV doesn't meet job requirements>],
            "key_skills": [<list of relevant skills found in CV>],
            "recommendation": <string with overall recommendation>
        }}
        
        Only return valid JSON, no other text."""
        
        response = ollama.chat(model='tinyllama:latest', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        # Extract and parse the JSON response
        try:
            analysis = json.loads(response['message']['content'].strip())
            # Ensure all required fields are present
            analysis = {
                'match_score': float(analysis.get('match_score', 0.0)),
                'strengths': analysis.get('strengths', []),
                'weaknesses': analysis.get('weaknesses', []),
                'key_skills': analysis.get('key_skills', []),
                'recommendation': analysis.get('recommendation', 'No recommendation available')
            }
            # Ensure match_score is between 0 and 1
            analysis['match_score'] = max(0.0, min(1.0, analysis['match_score']))
            return analysis
            
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Error parsing analysis: {str(e)}")
            return {
                'match_score': 0.0,
                'strengths': [],
                'weaknesses': ['Error analyzing CV'],
                'key_skills': [],
                'recommendation': 'Unable to analyze CV properly'
            }
            
    except Exception as e:
        print(f"Error in CV analysis: {str(e)}")
        return {
            'match_score': 0.0,
            'strengths': [],
            'weaknesses': ['Error analyzing CV'],
            'key_skills': [],
            'recommendation': f'Error during analysis: {str(e)}'
        }

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