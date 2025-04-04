# ai_job_screening.md

## Enhancing Job Screening with AI and Data Intelligence

### Project Overview
This project aims to develop a multi-agent AI system that automates recruitment tasks, including summarizing job descriptions (JDs), matching CVs to JDs, shortlisting candidates, and scheduling interviews.

### Agents and Responsibilities
1. **JD Summarizer**: Extracts skills, experience, and qualifications from JD text using the Ollama (Phi-2) model.
2. **CV Analyzer**: Extracts CV data and computes a match score (0-1) against the JD using Ollama.
3. **Shortlister**: Filters candidates with a match score >= 0.8 from SQLite.
4. **Scheduler**: Sends mock interview emails using smtplib.

### Tools and Technologies
- **Ollama (Phi-2 model)**: Handles NLP tasks for text extraction and analysis.
- **SQLite**: Stores JD summaries and candidate data in two tables: `jobs` and `candidates`.
- **Python 3.8+** with the following libraries:
  - `ollama` for NLP tasks
  - `sqlite3` for database management
  - `smtplib` for email handling

### Code Structure
```
project_root/
│── main.py  # Entry point to orchestrate all agents
│
├── agents/
│   ├── jd_summarizer.py  # Extracts key info from JD
│   ├── cv_analyzer.py  # Parses CVs and computes match score
│   ├── shortlister.py  # Shortlists candidates based on match score
│   ├── scheduler.py  # Sends mock interview emails
│
├── data/
│   ├── job_description.txt  # Sample JD
│   ├── candidate_cv.txt  # Sample CVs
│
├── database/
│   ├── recruitment.db  # SQLite database storing jobs and candidates
```

### Implementation Details
#### `jd_summarizer.py`
Extracts relevant job criteria using Ollama.
```python
import ollama
import sqlite3

def summarize_jd(jd_text):
    response = ollama.complete("Extract skills, experience, qualifications from the following JD: " + jd_text)
    return response

def store_jd(jd_text):
    summary = summarize_jd(jd_text)
    conn = sqlite3.connect("../database/recruitment.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (description, summary) VALUES (?, ?)", (jd_text, summary))
    conn.commit()
    conn.close()
```

#### `cv_analyzer.py`
Matches CVs against JDs and assigns a match score.
```python
import ollama
import sqlite3

def analyze_cv(cv_text, jd_summary):
    response = ollama.complete(f"Match the following CV against JD summary: {jd_summary}. Return a score (0-1).")
    return float(response) if response.replace('.', '', 1).isdigit() else 0.0

def store_candidate(cv_text, match_score):
    conn = sqlite3.connect("../database/recruitment.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidates (cv_text, match_score) VALUES (?, ?)", (cv_text, match_score))
    conn.commit()
    conn.close()
```

#### `shortlister.py`
Filters candidates based on match score.
```python
import sqlite3

def shortlist_candidates():
    conn = sqlite3.connect("../database/recruitment.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE match_score >= 0.8")
    shortlisted = cursor.fetchall()
    conn.close()
    return shortlisted
```

#### `scheduler.py`
Mocks interview scheduling via print statements.
```python
import smtplib

def send_mock_email(candidate_email):
    print(f"Mock email sent to {candidate_email}: 'You are shortlisted for an interview.'")
```

### Execution Flow
1. `jd_summarizer.py` processes JDs and stores summaries in SQLite.
2. `cv_analyzer.py` evaluates CVs against JDs and assigns match scores.
3. `shortlister.py` filters candidates with a match score ≥ 0.8.
4. `scheduler.py` sends interview invites to shortlisted candidates.

This modular structure ensures easy integration and scalability.






