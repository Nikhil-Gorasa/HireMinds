# AI-Powered Job Application Screening System

## Overview

This project implements an AI-powered system for screening job applications using Ollama for natural language processing. The system can process job descriptions and candidate CVs to match candidates with jobs and automatically shortlist the best matches.

## Features

- Import job descriptions from Excel/CSV files
- Import candidate CVs from PDF files
- AI-powered analysis of job descriptions and CVs
- Automatic candidate shortlisting based on match scores
- Interview scheduling for shortlisted candidates
- Real-time progress tracking and status updates

## Technical Stack

- Python 3.8+
- Flask web framework
- SQLAlchemy ORM
- Ollama for NLP
- Bootstrap 5 for UI
- JavaScript for frontend interactivity

## Installation

1. Clone the repository
2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:

   ```bash
   python init_db.py
   ```

## Usage

1. Start the Flask application:

   ```bash
   python run.py
   ```

2. Open your browser and navigate to `http://localhost:5000`
3. Import job descriptions using Excel/CSV files
4. Import candidate CVs using PDF files
5. Use the dashboard to monitor processing status
6. View and manage shortlisted candidates

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── job.py
│   │   ├── candidate.py
│   │   └── shortlisted_candidate.py
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── jobs.html
│       └── candidates.html
├── agents/
│   ├── __init__.py
│   ├── summarizer.py
│   ├── analyzer.py
│   ├── shortlister.py
│   └── scheduler.py
├── database/
│   ├── __init__.py
│   └── db.py
├── uploads/
├── requirements.txt
├── init_db.py
└── run.py
```

## API Endpoints

- `POST /api/import-jobs`: Import job descriptions
- `POST /api/import-cvs/<job_id>`: Import CVs for a specific job
- `POST /api/import-all-cvs`: Import CVs for all jobs
- `POST /api/shortlist-candidates/<job_id>`: Shortlist candidates for a job
- `POST /api/shortlist-all`: Shortlist candidates for all jobs
- `POST /api/schedule-interviews/<job_id>`: Schedule interviews for shortlisted candidates
- `POST /api/process-all`: Process all data (import jobs, CVs, and shortlist)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 