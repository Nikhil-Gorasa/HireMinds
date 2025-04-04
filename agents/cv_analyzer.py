import ollama
from database.db import db, Candidate, Job

def analyze_cv(cv_text, job_id):
    """Analyze CV against job requirements and compute match score."""
    try:
        job = Job.query.get(job_id)
        if not job:
            return None

        prompt = f"""Analyze this CV against the job requirements and provide a match score between 0 and 1.
        Consider the following aspects:
        1. Skills match
        2. Experience level
        3. Qualifications
        4. Overall fit
        
        Job Requirements:
        {job.summary}
        
        CV:
        {cv_text}
        
        Provide only a numerical score between 0 and 1, where 1 is perfect match."""
        
        response = ollama.chat(model='phi', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        # Extract numerical score from response
        score_text = response['message']['content'].strip()
        try:
            score = float(score_text)
        except ValueError:
            score = 0.0
            
        return score
    except Exception as e:
        print(f"Error in CV analysis: {str(e)}")
        return None

def store_candidate(name, cv_text, job_id):
    """Store candidate information and match score in the database."""
    try:
        match_score = analyze_cv(cv_text, job_id)
        candidate = Candidate(
            name=name,
            cv_text=cv_text,
            match_score=match_score,
            job_id=job_id
        )
        db.session.add(candidate)
        db.session.commit()
        return candidate
    except Exception as e:
        print(f"Error storing candidate: {str(e)}")
        db.session.rollback()
        return None 