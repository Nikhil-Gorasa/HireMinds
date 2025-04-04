import ollama
from database.db import db, Job

def summarize_jd(jd_text):
    """Extract key information from job description using Ollama."""
    prompt = f"""Extract the following information from this job description:
    1. Required skills
    2. Experience level
    3. Key responsibilities
    4. Qualifications
    
    Job Description:
    {jd_text}
    
    Format the response as a structured summary."""
    
    try:
        response = ollama.chat(model='phi', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        return response['message']['content']
    except Exception as e:
        print(f"Error in JD summarization: {str(e)}")
        return None

def store_jd(title, description):
    """Store job description and its summary in the database."""
    try:
        summary = summarize_jd(description)
        job = Job(title=title, description=description, summary=summary)
        db.session.add(job)
        db.session.commit()
        return job
    except Exception as e:
        print(f"Error storing JD: {str(e)}")
        db.session.rollback()
        return None 