"""Global configuration settings."""

# Ollama Model Configuration
OLLAMA_MODEL = "llama3:latest"  # Can be changed to 'llama2:latest', 'codellama:latest', etc.
OLLAMA_ENDPOINT = "http://127.0.0.1:11434"

# Analysis Settings
MAX_TEXT_LENGTH = 4000  # Maximum characters for CV and job description
BATCH_SIZE = 5  # Number of CVs to process in parallel

# Scoring Weights
SCORE_WEIGHTS = {
    'essential_skills': 0.4,
    'experience': 0.3,
    'education': 0.15,
    'additional': 0.15
}

# Technical Skills List
TECHNICAL_SKILLS = [
    'Python', 'Java', 'JavaScript', 'C++', 'SQL', 'AWS', 'Azure', 'Docker',
    'Kubernetes', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express', 'Django',
    'Flask', 'Spring', 'Git', 'CI/CD', 'Jenkins', 'Testing', 'Machine Learning',
    'AI', 'Data Analysis', 'Cloud', 'DevOps', 'Security', 'Linux', 'Windows',
    'Networking', 'API', 'REST', 'GraphQL', 'MongoDB', 'PostgreSQL', 'MySQL',
    'Oracle', 'HTML', 'CSS', 'PHP', 'Ruby', 'Scala', 'Hadoop', 'Spark',
    'TensorFlow', 'PyTorch', 'NLP', 'Computer Vision', 'Agile', 'Scrum'
]

# Soft Skills List
SOFT_SKILLS = [
    'Leadership', 'Communication', 'Problem Solving', 'Team Work', 'Time Management',
    'Project Management', 'Critical Thinking', 'Adaptability', 'Creativity',
    'Analytical Skills', 'Attention to Detail', 'Organization', 'Decision Making',
    'Interpersonal Skills', 'Presentation Skills', 'Negotiation', 'Mentoring'
]

# CV Analysis Template
CV_ANALYSIS_TEMPLATE = """You are an expert HR recruiter analyzing a CV against job requirements. Be objective and thorough.

Job Description:
%s

CV Content:
%s

Follow these strict scoring guidelines:

Essential Skills Match (40%% of total score):
- Compare required skills in job description with CV
- Award points for exact matches and relevant equivalents
- Consider both technical and soft skills
- Factor in skill proficiency levels when mentioned

Experience Relevance (30%% of total score):
- Years of relevant experience
- Industry relevance
- Project/role similarities
- Leadership/management requirements if applicable

Education Fit (15%% of total score):
- Required degree/certification matches
- Field of study relevance
- Additional relevant certifications
- Academic achievements if relevant

Additional Qualifications (15%% of total score):
- Extra relevant certifications
- Industry recognition
- Publications/patents if applicable
- Relevant achievements

Provide a JSON response with these fields:
{
    "match_score": <calculated score between 0-1>,
    "score_breakdown": {
        "essential_skills": <score 0-1>,
        "experience": <score 0-1>,
        "education": <score 0-1>,
        "additional": <score 0-1>
    },
    "strengths": [
        "specific strength 1",
        "specific strength 2"
    ],
    "weaknesses": [
        "specific weakness 1",
        "specific weakness 2"
    ],
    "key_skills": [
        "matched skill 1",
        "matched skill 2"
    ],
    "recommendation": "Detailed recommendation explaining score and key factors"
}

Important:
- Be specific about strengths and weaknesses
- List actual skills found in the CV that match job requirements
- Explain your scoring in the recommendation
- Ensure all scores are justified by evidence from CV and job description""" 