from ollama import Client
import json

def analyze_cv(cv_text, job_description):
    """Analyze a CV against a job description using Ollama."""
    try:
        client = Client()
        
        prompt = f"""Please analyze this CV against the job description and provide a detailed assessment:

Job Description:
{job_description}

CV Content:
{cv_text}

Format the response as a JSON object with the following structure:
{{
    "match_score": float between 0 and 1,
    "strengths": ["List of candidate's strengths"],
    "weaknesses": ["List of candidate's weaknesses"],
    "recommendation": "Brief recommendation",
    "key_skills": ["List of relevant skills found in CV"]
}}"""

        response = client.chat(model='tinyllama:latest', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        # Extract the JSON response
        try:
            result = json.loads(response['message']['content'])
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, return a simple analysis
            return {
                "match_score": 0.0,
                "strengths": [],
                "weaknesses": [],
                "recommendation": response['message']['content'],
                "key_skills": []
            }
            
    except Exception as e:
        print(f"Error in analyze_cv: {str(e)}")
        return {
            "match_score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendation": "Error analyzing CV",
            "key_skills": []
        } 