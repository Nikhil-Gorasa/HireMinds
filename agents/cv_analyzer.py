import ollama
from database.db import db
from app.models.candidate import Candidate
import json
import logging
import re
from typing import Dict, List, Union
from config import (
    OLLAMA_MODEL, OLLAMA_ENDPOINT, MAX_TEXT_LENGTH, BATCH_SIZE,
    SCORE_WEIGHTS, TECHNICAL_SKILLS, SOFT_SKILLS, CV_ANALYSIS_TEMPLATE
)
import asyncio
import httpx

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    # Remove extra whitespace and normalize line endings
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove any control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
    return text

def extract_name_from_cv(cv_text: str) -> str:
    """Try to extract candidate name from CV text."""
    # Look for common name patterns at the start of the CV
    first_lines = cv_text.split('\n')[:5]  # Check first 5 lines
    for line in first_lines:
        line = line.strip()
        # Skip lines that are too long (likely not a name)
        if len(line) > 50:
            continue
        # Skip lines with common words that aren't names
        if any(word in line.lower() for word in ['resume', 'cv', 'curriculum', 'vitae', 'address', 'phone', 'email']):
            continue
        # If we have a reasonable length line with 2-4 words, it's likely a name
        words = line.split()
        if 2 <= len(words) <= 4:
            return line
    return "Unnamed Candidate"

def extract_skills(text: str) -> List[str]:
    """Extract both technical and soft skills from text."""
    text = text.lower()
    skills = set()
    
    # Look for technical skills
    for skill in TECHNICAL_SKILLS:
        if skill.lower() in text:
            skills.add(skill)
    
    # Look for soft skills
    for skill in SOFT_SKILLS:
        if skill.lower() in text:
            skills.add(skill)
    
    return list(skills)

def calculate_skill_match(cv_skills: List[str], job_skills: List[str]) -> float:
    """Calculate skill match score between CV and job skills."""
    if not job_skills:
        return 0.5
    
    cv_skills_set = set(s.lower() for s in cv_skills)
    job_skills_set = set(s.lower() for s in job_skills)
    
    matches = cv_skills_set.intersection(job_skills_set)
    return len(matches) / len(job_skills_set) if job_skills_set else 0.5

async def analyze_cv_batch(cvs: List[Dict], job_description: str) -> List[Dict]:
    """Analyze a batch of CVs against a job description."""
    job_skills = extract_skills(job_description)
    
    async def process_single_cv(cv_data: Dict) -> Dict:
        try:
            cv_text = clean_text(cv_data['cv_text'])
            if len(cv_text) > MAX_TEXT_LENGTH:
                cv_text = cv_text[:MAX_TEXT_LENGTH]
            
            # Extract skills before LLM analysis
            cv_skills = extract_skills(cv_text)
            skill_match_score = calculate_skill_match(cv_skills, job_skills)
            
            # Prepare prompt
            prompt = CV_ANALYSIS_TEMPLATE % (job_description, cv_text)
            
            # Get LLM analysis
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_ENDPOINT}/api/chat",
                    json={
                        "model": OLLAMA_MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an expert HR recruiter. Return only valid JSON."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"API error: {response.status_code}")
                
                content = response.json()['message']['content'].strip()
                
                # Extract JSON from response
                json_match = re.search(r'\{[\s\S]*\}', content)
                if not json_match:
                    raise ValueError("No JSON found in response")
                
                analysis = json.loads(json_match.group(0))
                
                # Merge skill-based and LLM analysis
                analysis['match_score'] = round((skill_match_score + float(analysis['match_score'])) / 2, 2)
                analysis['key_skills'] = list(set(cv_skills))  # Use extracted skills
                
                if 'score_breakdown' not in analysis:
                    analysis['score_breakdown'] = {
                        'essential_skills': skill_match_score,
                        'experience': analysis.get('match_score', 0.5),
                        'education': 0.5,
                        'additional': 0.5
                    }
                
                return {
                    'candidate_id': cv_data.get('candidate_id'),
                    'name': cv_data.get('name', extract_name_from_cv(cv_text)),
                    'analysis': analysis
                }
                
        except Exception as e:
            logger.error(f"Error analyzing CV: {str(e)}")
            return {
                'candidate_id': cv_data.get('candidate_id'),
                'name': cv_data.get('name', "Unknown"),
                'analysis': {
                    'match_score': skill_match_score,
                    'score_breakdown': {
                        'essential_skills': skill_match_score,
                        'experience': 0.5,
                        'education': 0.5,
                        'additional': 0.5
                    },
                    'strengths': [f"Has skills: {', '.join(cv_skills[:3])}"] if cv_skills else ["Manual review needed"],
                    'weaknesses': ["Automated analysis failed"],
                    'key_skills': cv_skills,
                    'recommendation': f"Technical error - but found {len(cv_skills)} matching skills"
                }
            }
    
    # Process CVs in parallel
    tasks = [process_single_cv(cv) for cv in cvs]
    results = await asyncio.gather(*tasks)
    return results

def analyze_cvs(cvs: List[Dict], job_description: str) -> List[Dict]:
    """Analyze multiple CVs against a job description."""
    # Clean job description
    job_description = clean_text(job_description)
    if len(job_description) > MAX_TEXT_LENGTH:
        job_description = job_description[:MAX_TEXT_LENGTH]
    
    # Process CVs in batches
    results = []
    for i in range(0, len(cvs), BATCH_SIZE):
        batch = cvs[i:i + BATCH_SIZE]
        batch_results = asyncio.run(analyze_cv_batch(batch, job_description))
        results.extend(batch_results)
    
    return results

def store_candidate(name: str, cv_text: str, job_id: int, analysis: Dict = None) -> Candidate:
    """Store a candidate in the database with proper error handling."""
    try:
        logger.info(f"Storing candidate: {name} for job_id: {job_id}")
        
        # If no name provided, try to extract from CV
        if not name or name.strip() == "":
            name = extract_name_from_cv(cv_text)
        
        # Clean the CV text
        cv_text = clean_text(cv_text)
        
        # Create candidate with safe defaults if analysis is missing
        candidate = Candidate(
            name=name,
            cv_text=cv_text,
            job_id=job_id,
            analysis=json.dumps(analysis) if analysis else json.dumps({
                'match_score': 0.0,
                'strengths': ["Pending analysis"],
                'weaknesses': ["Pending analysis"],
                'key_skills': ["Pending analysis"],
                'recommendation': "Pending automated analysis"
            }),
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

def analyze_cv(cv_text: str, job_description: str) -> Dict:
    """Analyze a single CV against a job description (backward compatibility)."""
    try:
        # Clean and validate inputs
        cv_text = clean_text(cv_text)
        job_description = clean_text(job_description)
        
        if not cv_text or not job_description:
            raise ValueError("Empty CV text or job description")
        
        # Extract skills before LLM analysis
        cv_skills = extract_skills(cv_text)
        job_skills = extract_skills(job_description)
        skill_match_score = calculate_skill_match(cv_skills, job_skills)
        
        # Prepare prompt
        prompt = CV_ANALYSIS_TEMPLATE % (job_description, cv_text)
        
        # Get LLM analysis
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': 'You are an expert HR recruiter. Return only valid JSON.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        if not response or not isinstance(response, dict) or 'message' not in response:
            raise ValueError("Invalid API response")
        
        content = response['message']['content'].strip()
        
        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', content)
        if not json_match:
            raise ValueError("No JSON found in response")
        
        analysis = json.loads(json_match.group(0))
        
        # Validate analysis structure
        if not isinstance(analysis, dict):
            raise ValueError("Invalid analysis format")
        
        # Ensure all required fields exist
        required_fields = ['match_score', 'strengths', 'weaknesses', 'key_skills', 'recommendation']
        for field in required_fields:
            if field not in analysis:
                analysis[field] = []
        
        # Merge skill-based and LLM analysis
        analysis['match_score'] = round((skill_match_score + float(analysis.get('match_score', 0.5))) / 2, 2)
        analysis['key_skills'] = list(set(cv_skills))  # Use extracted skills
        
        if 'score_breakdown' not in analysis:
            analysis['score_breakdown'] = {
                'essential_skills': skill_match_score,
                'experience': analysis.get('match_score', 0.5),
                'education': 0.5,
                'additional': 0.5
            }
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error in CV analysis: {str(e)}")
        return {
            'match_score': skill_match_score,
            'score_breakdown': {
                'essential_skills': skill_match_score,
                'experience': 0.5,
                'education': 0.5,
                'additional': 0.5
            },
            'strengths': [f"Has skills: {', '.join(cv_skills[:3])}"] if cv_skills else ["Manual review needed"],
            'weaknesses': ["Automated analysis failed"],
            'key_skills': cv_skills,
            'recommendation': f"Technical error - but found {len(cv_skills)} matching skills"
        } 