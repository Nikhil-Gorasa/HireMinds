# HireMinds - AI-Powered Recruitment Platform

HireMinds is an intelligent recruitment platform that uses AI to analyze CVs, match candidates with jobs, and streamline the hiring process. The platform leverages Ollama's language models for advanced CV analysis and candidate matching.

## Features

- 📄 CV Analysis and Parsing
- 🎯 Job-Candidate Matching
- 📊 Candidate Scoring
- 📅 Interview Scheduling
- 👥 Shortlisting Management
- 📱 Modern Web Interface

## Prerequisites

Before you begin, ensure you have the following installed:

1. Python 3.8 or higher
2. Ollama (for AI model support)
3. Git
4. SQLite (included with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hireminds.git
cd hireminds
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama:
   - Visit [Ollama's official website](https://ollama.ai/download)
   - Download and install Ollama for your operating system
   - Start the Ollama service

5. Pull the required model:
```bash
ollama pull mistral:latest
```

## Configuration

1. Create a `.env` file in the root directory:
```env
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

2. Update the model settings in `config.py` if needed:
```python
OLLAMA_MODEL = "mistral:latest"  # Change this to use a different model
```

## Database Setup

1. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Application

1. Start the Flask development server:
```bash
flask run
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t hireminds .
```

2. Run the container:
```bash
docker run -p 5000:5000 hireminds
```

## Production Deployment

For production deployment, we recommend using:

1. Gunicorn as the WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

2. Nginx as the reverse proxy:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

1. If Ollama is not responding:
   - Ensure Ollama service is running
   - Check if the model is downloaded
   - Verify the endpoint in config.py

2. Database issues:
   - Check database migrations
   - Verify SQLite file permissions
   - Ensure proper database initialization

3. Application errors:
   - Check logs in `logs/app.log`
   - Verify environment variables
   - Ensure all dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 