from ollama import Client
import json

def summarize_job(job_description):
    """Generate a summary of the job description using Ollama."""
    try:
        client = Client()
        
        prompt = f"""Please provide a concise summary of this job description, highlighting the key requirements and responsibilities:

{job_description}

Format the response as a JSON object with the following structure:
{{
    "summary": "A brief summary of the job",
    "key_requirements": ["List of main requirements"],
    "key_responsibilities": ["List of main responsibilities"]
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
            # If JSON parsing fails, return a simple summary
            return {
                "summary": response['message']['content'],
                "key_requirements": [],
                "key_responsibilities": []
            }
            
    except Exception as e:
        print(f"Error in summarize_job: {str(e)}")
        return {
            "summary": "Error generating summary",
            "key_requirements": [],
            "key_responsibilities": []
        } 