from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from database.db import db
from app.models.job import Job
from app.models.candidate import Candidate
from app.models.shortlisted_candidate import ShortlistedCandidate
from agents.jd_summarizer import store_jd
from agents.cv_analyzer import analyze_cv, store_candidate
from agents.shortlister import shortlist_candidates, get_shortlisted_candidates
from agents.scheduler import schedule_interviews, get_scheduled_interviews
import pandas as pd
import os
from datetime import datetime, timezone, timedelta
from werkzeug.utils import secure_filename
import PyPDF2
import io
from PyPDF2 import PdfReader
from agents.summarizer import summarize_job
import json
import random

main = Blueprint('main', __name__)

# Get the absolute path to the uploads directory
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {
    'jobs': {'xlsx', 'xls', 'csv'},
    'cvs': {'pdf'}
}

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created uploads directory at: {UPLOAD_FOLDER}")

def allowed_file(filename, file_type):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]

def read_pdf(file):
    """Extract text from PDF file."""
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None

def get_dataset_path():
    """Get the path to the dataset directory."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                       '[Usecase 5] AI-Powered Job Application Screening System Dataset')

@main.route('/')
def index():
    """Render the dashboard with jobs, candidates, and shortlisted candidates."""
    jobs = Job.query.all()
    candidates = Candidate.query.all()
    shortlisted = ShortlistedCandidate.query.all()
    return render_template('dashboard.html', jobs=jobs, candidates=candidates, shortlisted=shortlisted)

@main.route('/jobs')
def jobs():
    """Render the jobs page."""
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)

@main.route('/candidates/<int:job_id>')
def candidates(job_id):
    """Render the candidates page for a specific job."""
    job = Job.query.get_or_404(job_id)
    candidates = Candidate.query.filter_by(job_id=job_id).all()
    shortlisted = get_shortlisted_candidates(job_id)
    return render_template('candidates.html', job=job, candidates=candidates, shortlisted=shortlisted)

@main.route('/api/import-jobs', methods=['POST'])
def import_jobs():
    """Import jobs from the uploaded Excel file."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename, 'jobs'):
        return jsonify({'success': False, 'error': 'Invalid file type. Please upload an Excel or CSV file.'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        if filename.endswith('.csv'):
            # Try different encodings
            encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(filepath, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                return jsonify({
                    'success': False,
                    'error': 'Could not read the CSV file. Please ensure it is properly encoded.'
                }), 400
        else:
            df = pd.read_excel(filepath)
        
        # Check for required columns
        required_columns = ['Job Title', 'Job Description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({
                'success': False,
                'error': f'Missing required columns: {", ".join(missing_columns)}'
            }), 400
        
        jobs_created = 0
        for _, row in df.iterrows():
            if pd.isna(row['Job Description']):
                continue
                
            # Clean the text by removing special characters and triple quotes
            title = str(row['Job Title']).strip() if not pd.isna(row['Job Title']) else 'Untitled Job'
            description = str(row['Job Description']).strip()
            
            # Extract requirements from description if not provided
            requirements = str(row.get('Requirements', description)).strip()
            
            # Remove triple quotes and clean text
            title = title.replace("'''", "").replace("''", "'").replace("'", "'")
            description = description.replace("'''", "").replace("''", "'").replace("'", "'")
            requirements = requirements.replace("'''", "").replace("''", "'").replace("'", "'")
            
            job = Job(
                title=title,
                description=description,
                requirements=requirements,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(job)
            jobs_created += 1
        
        db.session.commit()
        os.remove(filepath)
        return jsonify({
            'success': True,
            'message': f'Successfully imported {jobs_created} jobs'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error importing jobs: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/import-cvs', methods=['POST'])
def import_cvs():
    if 'files' not in request.files:
        return jsonify({
            'success': False,
            'message': 'No files provided'
        })
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({
            'success': False,
            'message': 'No files selected'
        })
    
    job_id = request.form.get('job_id')
    if not job_id:
        return jsonify({
            'success': False,
            'message': 'No job ID provided'
        })
    
    job = Job.query.get(job_id)
    if not job:
        return jsonify({
            'success': False,
            'message': 'Job not found'
        })
    
    processed_count = 0
    for file in files:
        if file and file.filename.endswith('.pdf'):
            try:
                # Read PDF file
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Analyze CV
                analysis = analyze_cv(text, job.description)
                
                # Create candidate
                candidate = Candidate(
                    name=file.filename.replace('.pdf', ''),
                    cv_text=text,
                    analysis=json.dumps(analysis),
                    match_score=analysis.get('match_score', 0.0),
                    job_id=job_id
                )
                db.session.add(candidate)
                processed_count += 1
                
            except Exception as e:
                print(f"Error processing file {file.filename}: {str(e)}")
                continue
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Successfully processed {processed_count} CVs'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error saving candidates: {str(e)}'
        })

@main.route('/api/import-all-cvs', methods=['POST'])
def import_all_cvs():
    if 'files' not in request.files:
        return jsonify({
            'success': False,
            'message': 'No files provided'
        })
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({
            'success': False,
            'message': 'No files selected'
        })
    
    processed_count = 0
    for file in files:
        if file and file.filename.endswith('.pdf'):
            try:
                # Read PDF file
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Get all jobs
                jobs = Job.query.all()
                
                for job in jobs:
                    # Analyze CV against each job
                    analysis = analyze_cv(text, job.description)
                    
                    # Create candidate
                    candidate = Candidate(
                        name=file.filename.replace('.pdf', ''),
                        cv_text=text,
                        analysis=json.dumps(analysis),
                        match_score=analysis.get('match_score', 0.0),
                        job_id=job.id
                    )
                    db.session.add(candidate)
                    processed_count += 1
                
            except Exception as e:
                print(f"Error processing file {file.filename}: {str(e)}")
                continue
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Successfully processed {processed_count} CVs'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error saving candidates: {str(e)}'
        })

@main.route('/api/shortlist-candidates/<int:job_id>', methods=['POST'])
def shortlist_candidates_route(job_id):
    """Shortlist candidates for a specific job."""
    try:
        data = request.get_json()
        count = data.get('count', 5)  # Default to top 5 if not specified
        
        # Get all candidates for the job, sorted by match score
        candidates = Candidate.query.filter_by(job_id=job_id).order_by(Candidate.match_score.desc()).all()
        
        # Update status for all candidates
        for i, candidate in enumerate(candidates):
            analysis = json.loads(candidate.analysis)
            if i < count and candidate.match_score >= 0.45:  # Only shortlist if score is at least 0.45
                status = 'Selected'
            else:
                status = 'Rejected'
            
            # Create or update shortlisted candidate
            shortlisted = ShortlistedCandidate.query.filter_by(
                job_id=job_id,
                candidate_id=candidate.id
            ).first()
            
            if not shortlisted:
                shortlisted = ShortlistedCandidate(
                    job_id=job_id,
                    candidate_id=candidate.id,
                    status=status
                )
                db.session.add(shortlisted)
            else:
                shortlisted.status = status
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Successfully shortlisted top {count} candidates',
            'selected': count,
            'total': len(candidates)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/shortlist-all', methods=['POST'])
def shortlist_all_candidates():
    """Shortlist candidates for all jobs."""
    jobs = Job.query.all()
    total_shortlisted = 0
    
    try:
        for job in jobs:
            count = shortlist_candidates(job.id)
            total_shortlisted += count
        
        return jsonify({
            'message': f'Successfully shortlisted {total_shortlisted} candidates across all jobs'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/shortlisted/<int:job_id>')
def get_shortlisted(job_id):
    """Get shortlisted candidates for a specific job."""
    shortlisted = ShortlistedCandidate.query.filter_by(job_id=job_id).all()
    return jsonify([{
        'id': s.id,
        'candidate_name': s.get_candidate_name(),
        'interview_date': s.interview_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': s.status
    } for s in shortlisted])

@main.route('/api/candidate-cv/<int:candidate_id>')
def get_candidate_cv(candidate_id):
    """Get candidate details including CV text and match score."""
    candidate = Candidate.query.get_or_404(candidate_id)
    return jsonify({
        'cv_text': candidate.cv_text,
        'analysis': candidate.analysis
    })

@main.route('/api/schedule-interviews/<int:job_id>', methods=['POST'])
def schedule_interviews_route(job_id):
    try:
        count = schedule_interviews(job_id)
        return jsonify({'success': True, 'message': f'Successfully scheduled {count} interviews'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error scheduling interviews: {str(e)}'})

@main.route('/api/process-all', methods=['POST'])
def process_all():
    try:
        # Import jobs
        jobs_response = import_jobs()
        if not jobs_response.json['success']:
            return jobs_response
        
        # Import CVs
        cvs_response = import_all_cvs()
        if not cvs_response.json['success']:
            return cvs_response
        
        # Shortlist candidates
        shortlist_response = shortlist_all_candidates()
        if not shortlist_response.json['success']:
            return shortlist_response
        
        return jsonify({'success': True, 'message': 'Successfully processed all data'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error processing data: {str(e)}'})

@main.route('/api/delete-job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a specific job and its associated candidates."""
    try:
        job = Job.query.get_or_404(job_id)
        # Delete associated candidates
        Candidate.query.filter_by(job_id=job_id).delete()
        # Delete associated shortlisted candidates
        ShortlistedCandidate.query.filter_by(job_id=job_id).delete()
        # Delete the job
        db.session.delete(job)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Job deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/delete-all-jobs', methods=['DELETE'])
def delete_all_jobs():
    """Delete all jobs and their associated candidates."""
    try:
        # Delete all candidates
        Candidate.query.delete()
        # Delete all shortlisted candidates
        ShortlistedCandidate.query.delete()
        # Delete all jobs
        Job.query.delete()
        db.session.commit()
        return jsonify({'success': True, 'message': 'All jobs deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/delete-candidate/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """Delete a single candidate."""
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        db.session.delete(candidate)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Candidate deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/delete-candidates', methods=['DELETE'])
def delete_candidates():
    """Delete multiple candidates."""
    try:
        data = request.get_json()
        candidate_ids = data.get('candidate_ids', [])
        
        if not candidate_ids:
            return jsonify({'success': False, 'error': 'No candidates specified'}), 400
            
        Candidate.query.filter(Candidate.id.in_(candidate_ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'success': True, 'message': f'{len(candidate_ids)} candidates deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/delete-all-candidates/<int:job_id>', methods=['DELETE'])
def delete_all_candidates(job_id):
    """Delete all candidates for a job."""
    try:
        # Delete all candidates for the job
        Candidate.query.filter_by(job_id=job_id).delete()
        db.session.commit()
        return jsonify({'success': True, 'message': 'All candidates deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/reanalyze-candidates/<int:job_id>', methods=['POST'])
def reanalyze_candidates(job_id):
    """Reanalyze all CVs for a job."""
    try:
        job = Job.query.get_or_404(job_id)
        candidates = Candidate.query.filter_by(job_id=job_id).all()
        
        for candidate in candidates:
            # Reanalyze the CV
            analysis = analyze_cv(candidate.cv_text, job.description)
            candidate.analysis = json.dumps(analysis)
            candidate.match_score = analysis.get('match_score', 0.0)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Successfully reanalyzed {len(candidates)} candidates'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/send-interview-invite/<int:candidate_id>', methods=['POST'])
def send_interview_invite(candidate_id):
    """Send interview invite to a single candidate."""
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        meeting_data = request.get_json()
        
        # Send the invite
        candidate.send_interview_invite(meeting_data)
        
        return jsonify({
            'success': True,
            'message': f'Interview invite sent to {candidate.name}'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to send invite: {str(e)}'
        }), 500

@main.route('/api/send-all-invites', methods=['POST'])
def send_all_invites():
    """Send interview invites to all selected candidates."""
    try:
        meeting_data = request.get_json()
        job_id = request.args.get('job_id')
        
        # Get all selected candidates
        candidates = Candidate.query.filter(
            Candidate.job_id == job_id,
            Candidate.shortlisted == True
        ).all()
        
        sent_count = 0
        errors = []
        
        for candidate in candidates:
            try:
                candidate.send_interview_invite(meeting_data)
                sent_count += 1
            except Exception as e:
                errors.append(f"Failed to send to {candidate.name}: {str(e)}")
        
        return jsonify({
            'success': True,
            'sent': sent_count,
            'total': len(candidates),
            'errors': errors,
            'message': f'Successfully sent {sent_count} out of {len(candidates)} invites'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to send invites: {str(e)}'
        }), 500

@main.route('/api/schedule-interviews', methods=['POST'])
def schedule_interviews():
    """Schedule interviews for multiple candidates with automatic meeting link generation."""
    try:
        data = request.get_json()
        start_datetime = datetime.fromisoformat(data['startDateTime'])
        meeting_duration = int(data['meetingDuration'])
        break_duration = int(data['breakDuration'])
        additional_notes = data.get('additionalNotes', '')
        candidate_ids = data['candidateIds']
        job_id = data.get('job_id')

        if not job_id:
            return jsonify({
                'success': False,
                'error': 'Job ID is required'
            }), 400

        # Get all candidates
        candidates = Candidate.query.filter(
            Candidate.id.in_(candidate_ids),
            Candidate.job_id == job_id
        ).all()
        
        # Sort candidates by match score to prioritize higher scoring candidates
        candidates.sort(key=lambda x: x.match_score, reverse=True)
        
        scheduled_count = 0
        current_datetime = start_datetime
        
        for candidate in candidates:
            try:
                # Generate unique meeting link using Google Meet-like format
                meeting_id = ''.join(random.choices('abcdefghijkmnpqrstuvwxyz23456789', k=10))
                meeting_link = f"https://meet.google.com/{meeting_id}"
                
                # Format the email with personalized message
                personalized_notes = additional_notes.replace('{name}', candidate.name)
                
                meeting_data = {
                    'meetingDate': current_datetime.strftime('%Y-%m-%d %H:%M'),
                    'meetingDuration': meeting_duration,
                    'meetingLink': meeting_link,
                    'additionalNotes': f"""Dear {candidate.name},

We are pleased to invite you for an interview. Your interview has been scheduled for:

Date: {current_datetime.strftime('%A, %B %d, %Y')}
Time: {current_datetime.strftime('%I:%M %p')}
Duration: {meeting_duration} minutes

Meeting Link: {meeting_link}

{personalized_notes}

Please ensure you:
1. Test your audio and video before the interview
2. Join the meeting 5 minutes early
3. Have a stable internet connection
4. Keep your CV and portfolio ready

If you need to reschedule, please contact us at least 24 hours before the interview.

Best regards,
{current_app.config.get('COMPANY_NAME', 'Our')} Recruitment Team"""
                }
                
                # Send the invite
                candidate.send_interview_invite(meeting_data)
                
                # Update candidate status
                shortlisted = ShortlistedCandidate.query.filter_by(
                    candidate_id=candidate.id,
                    job_id=job_id
                ).first()
                
                if shortlisted:
                    shortlisted.interview_date = current_datetime
                    shortlisted.status = 'Scheduled'
                
                scheduled_count += 1
                
                # Add duration and break for next interview
                current_datetime += timedelta(minutes=meeting_duration + break_duration)
                
            except Exception as e:
                current_app.logger.error(f"Error scheduling interview for {candidate.name}: {str(e)}")
                continue
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully scheduled {scheduled_count} interviews',
            'scheduled': scheduled_count,
            'total': len(candidates)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to schedule interviews: {str(e)}'
        }), 500

@main.route('/interviews')
def interviews():
    """Render the interviews page showing all scheduled interviews."""
    # Get all shortlisted candidates with scheduled interviews
    interviews = ShortlistedCandidate.query.join(
        ShortlistedCandidate.candidate
    ).join(
        ShortlistedCandidate.job
    ).filter(
        ShortlistedCandidate.status == 'Scheduled',
        ShortlistedCandidate.interview_date.isnot(None)
    ).order_by(ShortlistedCandidate.interview_date.asc()).all()
    
    return render_template('interviews.html', interviews=interviews)

@main.route('/api/reschedule-interview/<int:interview_id>', methods=['POST'])
def reschedule_interview(interview_id):
    """Reschedule an interview."""
    try:
        data = request.get_json()
        new_datetime = datetime.fromisoformat(data['newDateTime'])
        
        interview = ShortlistedCandidate.query.get_or_404(interview_id)
        interview.interview_date = new_datetime
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Interview rescheduled successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to reschedule interview: {str(e)}'
        }), 500

@main.route('/api/cancel-interview/<int:interview_id>', methods=['POST'])
def cancel_interview(interview_id):
    """Cancel an interview."""
    try:
        interview = ShortlistedCandidate.query.get_or_404(interview_id)
        interview.status = 'Cancelled'
        interview.interview_date = None
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Interview cancelled successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to cancel interview: {str(e)}'
        }), 500 