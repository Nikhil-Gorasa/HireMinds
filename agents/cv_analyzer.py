import ollama
from database.db import db
from app.models.candidate import Candidate
import json

def analyze_cv(cv_text, job_description):
    """Analyze a CV against a job description using Ollama."""
    try:
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

        response = ollama.chat(model='tinyllama:latest', messages=[
            {
                'role': 'system',
                'content': 'You are an expert HR recruiter who analyzes CVs and provides structured assessments.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        # Extract and clean the JSON response
        try:
            content = response['message']['content'].strip()
            # Find the first { and last }
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
                analysis = json.loads(json_str)
                
                # Validate and ensure all required fields are present
                analysis = {
                    'match_score': float(min(max(analysis.get('match_score', 0.0), 0.0), 1.0)),
                    'strengths': analysis.get('strengths', ["No specific strengths identified"]),
                    'weaknesses': analysis.get('weaknesses', ["No specific areas for improvement identified"]),
                    'key_skills': analysis.get('key_skills', ["No specific skills identified"]),
                    'recommendation': analysis.get('recommendation', "Manual review recommended")
                }
                
                # Ensure lists are not empty
                for key in ['strengths', 'weaknesses', 'key_skills']:
                    if not analysis[key]:
                        analysis[key] = [f"No {key[:-1] if key.endswith('s') else key} identified"]
                
                return analysis
            
            raise ValueError("Could not find valid JSON in response")
            
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Error parsing analysis: {str(e)}")
            return {
                'match_score': 0.5,
                'strengths': ["CV requires manual review"],
                'weaknesses': ["Could not automatically analyze skills"],
                'key_skills': ["Manual skill assessment needed"],
                'recommendation': "Please review CV manually"
            }
            
    except Exception as e:
        print(f"Error in CV analysis: {str(e)}")
        return {
            'match_score': 0.0,
            'strengths': ["Error occurred during analysis"],
            'weaknesses': ["Could not complete automated analysis"],
            'key_skills': [],
            'recommendation': f"Technical error - please review manually: {str(e)}"
        }

def store_candidate(name, cv_text, job_id, analysis=None):
    """Store a candidate in the database."""
    try:
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
    except Exception as e:
        print(f"Error storing candidate: {str(e)}")
        db.session.rollback()
        raise 