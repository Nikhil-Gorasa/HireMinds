from ollama import Client
import json

def analyze_cv(cv_text, job_description):
    """Analyze a CV against a job description using Ollama."""
    try:
        client = Client()
        
        prompt = f"""You are an expert HR recruiter analyzing CVs. Evaluate this CV against the job description and provide a structured assessment.

Job Description:
{job_description}

CV Content:
{cv_text}

Analyze the CV and provide:
1. Calculate a match score (0-1) based on:
   - Required skills match
   - Experience relevance
   - Education fit
   - Overall suitability
2. List specific strengths found in the CV that match the job requirements
3. List specific areas where the candidate needs improvement
4. List concrete skills found in the CV
5. Provide a clear hiring recommendation

Return ONLY a JSON object with exactly this structure:
{{
    "match_score": <score between 0.0 and 1.0>,
    "strengths": ["specific strength 1", "specific strength 2"],
    "weaknesses": ["specific area for improvement 1", "specific area for improvement 2"],
    "key_skills": ["specific skill 1", "specific skill 2"],
    "recommendation": "Clear recommendation on whether to proceed with the candidate"
}}

Focus on concrete, specific points. Do not include example code or explanations."""

        # Use a more capable model
        response = client.chat(model='mistral:latest', messages=[
            {
                'role': 'system',
                'content': 'You are an expert HR recruiter who analyzes CVs and provides structured assessments.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        # Extract the JSON response
        try:
            # Clean the response to extract only the JSON part
            content = response['message']['content']
            # Find the first { and last }
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
                result = json.loads(json_str)
                
                # Validate and clean the result
                required_keys = ['match_score', 'strengths', 'weaknesses', 'recommendation', 'key_skills']
                if all(key in result for key in required_keys):
                    # Ensure match_score is a float between 0 and 1
                    result['match_score'] = float(min(max(result.get('match_score', 0.0), 0.0), 1.0))
                    # Ensure lists are not empty
                    result['strengths'] = result['strengths'] or ["No specific strengths identified"]
                    result['weaknesses'] = result['weaknesses'] or ["No specific areas for improvement identified"]
                    result['key_skills'] = result['key_skills'] or ["No specific skills identified"]
                    # Ensure recommendation is not empty
                    if not result['recommendation']:
                        result['recommendation'] = "Manual review recommended"
                    return result
            
            # If JSON parsing fails or structure is invalid, return a default analysis
            return {
                "match_score": 0.5,
                "strengths": ["CV requires manual review"],
                "weaknesses": ["Could not automatically analyze skills"],
                "recommendation": "Please review CV manually",
                "key_skills": ["Manual skill assessment needed"]
            }
        except json.JSONDecodeError:
            return {
                "match_score": 0.5,
                "strengths": ["CV requires manual review"],
                "weaknesses": ["Could not parse automated analysis"],
                "recommendation": "Please review CV manually",
                "key_skills": ["Manual skill assessment needed"]
            }
            
    except Exception as e:
        print(f"Error in analyze_cv: {str(e)}")
        return {
            "match_score": 0.0,
            "strengths": ["Error occurred during analysis"],
            "weaknesses": ["Could not complete automated analysis"],
            "recommendation": "Technical error - please review manually",
            "key_skills": []
        } 