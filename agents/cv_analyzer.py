import ollama
from database.db import db
from app.models.candidate import Candidate
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_cv(cv_text, job_description):
    """Analyze a CV against a job description using Ollama."""
    try:
        # Log input lengths to debug potential truncation issues
        logger.info(f"Processing CV analysis - CV length: {len(cv_text)}, Job desc length: {len(job_description)}")
        
        # Truncate texts if they're too long to avoid model context limits
        max_length = 4000
        if len(cv_text) > max_length:
            logger.warning(f"CV text truncated from {len(cv_text)} to {max_length} characters")
            cv_text = cv_text[:max_length]
        if len(job_description) > max_length:
            logger.warning(f"Job description truncated from {len(job_description)} to {max_length} characters")
            job_description = job_description[:max_length]

        prompt = f"""You are a strict HR recruiter with high standards. Analyze this CV against the job requirements.

Job Description:
{job_description}

CV Content:
{cv_text}

Use these strict criteria for scoring:
1. Essential skills match (40% of score)
2. Experience relevance (30% of score)
3. Education fit (15% of score)
4. Additional qualifications (15% of score)

A score above 0.75 is considered excellent
A score between 0.6-0.75 is good
A score between 0.45-0.6 needs careful consideration
A score below 0.45 is generally not recommended

Provide a JSON response with ONLY these fields:
{{
    "match_score": <number between 0.0 and 1.0>,
    "strengths": ["strength 1", "strength 2", ...],
    "weaknesses": ["weakness 1", "weakness 2", ...],
    "key_skills": ["skill 1", "skill 2", ...],
    "recommendation": "clear hiring recommendation with specific reasons"
}}

Return ONLY the JSON object, no other text or explanation."""

        # Make API call with timeout and retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1} of {max_retries}")
                response = ollama.chat(model='tinyllama:latest', messages=[
                    {
                        'role': 'system',
                        'content': 'You are an expert HR recruiter. Respond only with the requested JSON format.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ])
                
                content = response['message']['content'].strip()
                logger.info(f"Raw response received: {content[:200]}...")  # Log first 200 chars
                
                # Extract JSON from response
                start = content.find('{')
                end = content.rfind('}') + 1
                
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    logger.info(f"Extracted JSON: {json_str[:200]}...")
                    
                    analysis = json.loads(json_str)
                    
                    # Validate all required fields are present
                    required_fields = {'match_score', 'strengths', 'weaknesses', 'key_skills', 'recommendation'}
                    if not all(field in analysis for field in required_fields):
                        missing = required_fields - set(analysis.keys())
                        logger.error(f"Missing required fields: {missing}")
                        raise ValueError(f"Missing required fields: {missing}")
                    
                    # Clean and validate the response
                    cleaned = {
                        'match_score': float(min(max(float(analysis['match_score']), 0.0), 1.0)),
                        'strengths': analysis['strengths'][:5] if analysis['strengths'] else ["No specific strengths identified"],
                        'weaknesses': analysis['weaknesses'][:5] if analysis['weaknesses'] else ["No specific weaknesses identified"],
                        'key_skills': analysis['key_skills'][:10] if analysis['key_skills'] else ["No specific skills identified"],
                        'recommendation': str(analysis['recommendation']) or "Manual review recommended"
                    }
                    
                    # Validate lists contain actual values
                    for key in ['strengths', 'weaknesses', 'key_skills']:
                        cleaned[key] = [str(item) for item in cleaned[key] if item and str(item).strip()]
                        if not cleaned[key]:
                            cleaned[key] = [f"No {key[:-1] if key.endswith('s') else key} identified"]
                    
                    logger.info("Successfully analyzed CV")
                    return cleaned
                
                logger.error("No valid JSON found in response")
                if attempt < max_retries - 1:
                    continue
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {str(e)}")
                if attempt < max_retries - 1:
                    continue
            except Exception as e:
                logger.error(f"Error during analysis attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    continue
        
        # If all retries failed, return a default response
        logger.error("All analysis attempts failed")
        return {
            'match_score': 0.5,
            'strengths': ["Analysis failed - requires manual review"],
            'weaknesses': ["Could not automatically analyze skills"],
            'key_skills': ["Manual skill assessment needed"],
            'recommendation': "Please review CV manually due to analysis failure"
        }
            
    except Exception as e:
        logger.error(f"Critical error in CV analysis: {str(e)}")
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
        logger.info(f"Storing candidate: {name} for job_id: {job_id}")
        candidate = Candidate(
            name=name,
            cv_text=cv_text,
            job_id=job_id,
            analysis=json.dumps(analysis) if analysis else None,
            match_score=analysis.get('match_score', 0.0) if analysis else 0.0
        )
        db.session.add(candidate)
        db.session.commit()
        logger.info(f"Successfully stored candidate {name}")
        return candidate
    except Exception as e:
        logger.error(f"Error storing candidate {name}: {str(e)}")
        db.session.rollback()
        raise 