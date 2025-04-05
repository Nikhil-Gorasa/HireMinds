# HireMinds - AI-Powered Recruitment Platform

A modern web application for CV analysis and candidate matching using AI.

## Features

- CV Analysis
- Job-Candidate Matching
- Interview Scheduling
- AI-Powered Insights

## Prerequisites

- Python 3.8 or higher
- Ollama (for local AI processing)
- Git
- SQLite (for local development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hireminds.git
cd hireminds
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama:
   - Visit [Ollama.ai](https://ollama.ai) to download and install Ollama
   - Pull the required model:
   ```bash
   ollama pull mistral
   ```

5. Create a `.env` file:
```bash
cp .env.example .env
```

6. Update the `.env` file with your settings:
```env
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-generated-secret-key-here
OLLAMA_API_URL=http://localhost:11434
```

7. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Application

1. Start Ollama:
```bash
ollama serve
```

2. In a new terminal, start the Flask application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Important Note

This is a frontend-only deployment on Render.com. The AI processing features require Ollama to be running locally on your machine. When using the application:

1. The frontend will be hosted on Render.com
2. AI processing will be handled by your local Ollama instance
3. Make sure Ollama is running and accessible at `http://localhost:11434`

## Troubleshooting

### Ollama Issues
- Ensure Ollama is running (`ollama serve`)
- Check if the model is pulled (`ollama list`)
- Verify the API URL in your `.env` file

### Database Issues
- Check if the database is initialized
- Verify database migrations are up to date

### Application Issues
- Check the logs for error messages
- Verify all environment variables are set correctly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository. 