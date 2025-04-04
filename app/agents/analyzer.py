from ollama import Client
import json

def analyze_cv(cv_text, job_description):
    """Analyze a CV against a job description using Ollama."""
    client = Client()
    
    prompt = f"""Analyze this candidate's CV against the job description and provide a detailed analysis.
    
Job Description:
{job_description}

CV Text:
{cv_text}

Please provide a JSON response with the following structure:
{{
    "match_score": float between 0 and 1,
    "strengths": list of key strengths,
    "weaknesses": list of areas for improvement,
    "recommendations": list of recommendations,
    "key_skills": list of key skills found
}}

Focus on matching skills, experience, and qualifications. The match score should reflect how well the candidate matches the job requirements."""

    try:
        response = client.chat(model='phi', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        # Extract the JSON response from the message
        try:
            analysis = json.loads(response['message']['content'])
            return analysis
        except json.JSONDecodeError:
            # If JSON parsing fails, return a default analysis
            return {
                "match_score": 0.0,
                "strengths": ["Unable to analyze strengths"],
                "weaknesses": ["Unable to analyze weaknesses"],
                "recommendations": ["Unable to provide recommendations"],
                "key_skills": ["Unable to identify key skills"]
            }
            
    except Exception as e:
        print(f"Error in CV analysis: {str(e)}")
        return {
            "match_score": 0.0,
            "strengths": ["Error in analysis"],
            "weaknesses": ["Error in analysis"],
            "recommendations": ["Error in analysis"],
            "key_skills": ["Error in analysis"]
        } 