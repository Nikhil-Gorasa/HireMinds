import ollama
from database.db import db
from app.models.job import Job

def summarize_jd(jd_text):
    """Extract key information from job description using Ollama."""
    try:
        prompt = f"""Extract the following information from this job description:
        1. Required skills
        2. Required experience
        3. Required qualifications
        4. Key responsibilities
        
        Job Description:
        {jd_text}
        
        Format the response in a clear, structured way."""
        
        response = ollama.chat(model='tinyllama:latest', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        return response['message']['content']
    except Exception as e:
        print(f"Error in JD summarization: {str(e)}")
        return "Error analyzing job description"

def store_jd(title, description):
    """Store a job description in the database."""
    job = Job(title=title, description=description)
    db.session.add(job)
    db.session.commit()
    return job 