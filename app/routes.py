from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from database.db import db, Job, Candidate, ShortlistedCandidate
from agents.jd_summarizer import store_jd
from agents.cv_analyzer import store_candidate
from agents.shortlister import shortlist_candidates, get_shortlisted_candidates
import csv
import os
from datetime import datetime

main = Blueprint('main', __name__)

def get_dataset_path():
    """Get the path to the dataset directory."""
    return os.path.join(current_app.root_path, '..', '[Usecase 5] AI-Powered Job Application Screening System Dataset')

@main.route('/')
def index():
    jobs = Job.query.all()
    candidates = Candidate.query.all()
    shortlisted = ShortlistedCandidate.query.all()
    return render_template('dashboard.html', 
                         jobs=jobs, 
                         candidates=candidates, 
                         shortlisted=shortlisted,
                         interviews=shortlisted)

@main.route('/jobs')
def jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)

@main.route('/candidates/<int:job_id>')
def candidates(job_id):
    job = Job.query.get_or_404(job_id)
    candidates = Candidate.query.filter_by(job_id=job_id).all()
    return render_template('candidates.html', job=job, candidates=candidates)

@main.route('/api/import-jobs', methods=['POST'])
def import_jobs():
    try:
        # Clear existing jobs
        Job.query.delete()
        db.session.commit()
        
        # Read job descriptions from CSV
        csv_path = os.path.join(get_dataset_path(), 'job_description.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                job = Job(
                    title=row['title'],
                    description=row['description'],
                    summary=row.get('summary', '')
                )
                db.session.add(job)
        
        db.session.commit()
        return jsonify({'message': 'Jobs imported successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/import-cvs/<int:job_id>', methods=['POST'])
def import_cvs(job_id):
    try:
        # Clear existing candidates for this job
        Candidate.query.filter_by(job_id=job_id).delete()
        db.session.commit()
        
        # Read CVs from directory
        cv_dir = os.path.join(get_dataset_path(), 'CVs1')
        
        for filename in os.listdir(cv_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(cv_dir, filename), 'r', encoding='utf-8') as f:
                    cv_text = f.read()
                    candidate = Candidate(
                        name=filename.replace('.txt', ''),
                        cv_text=cv_text,
                        job_id=job_id,
                        match_score=0.0  # Will be updated by AI processing
                    )
                    db.session.add(candidate)
        
        db.session.commit()
        return jsonify({'message': 'CVs imported successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/shortlist-all', methods=['POST'])
def shortlist_all():
    try:
        # Clear all existing shortlisted candidates
        ShortlistedCandidate.query.delete()
        db.session.commit()
        
        total_shortlisted = 0
        jobs = Job.query.all()
        
        for job in jobs:
            candidates = Candidate.query.filter_by(job_id=job.id).all()
            for candidate in candidates:
                if candidate.match_score >= 80.0:  # 80% match threshold
                    shortlisted = ShortlistedCandidate(
                        candidate_id=candidate.id,
                        job_id=job.id,
                        interview_date=datetime.utcnow(),
                        status='scheduled'
                    )
                    db.session.add(shortlisted)
                    total_shortlisted += 1
        
        db.session.commit()
        return jsonify({'message': f'Shortlisted {total_shortlisted} candidates'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/shortlist/<int:job_id>', methods=['POST'])
def shortlist_job(job_id):
    try:
        # Clear existing shortlisted candidates for this job
        ShortlistedCandidate.query.filter_by(job_id=job_id).delete()
        db.session.commit()
        
        shortlisted_count = 0
        candidates = Candidate.query.filter_by(job_id=job_id).all()
        
        for candidate in candidates:
            if candidate.match_score >= 80.0:  # 80% match threshold
                shortlisted = ShortlistedCandidate(
                    candidate_id=candidate.id,
                    job_id=job_id,
                    interview_date=datetime.utcnow(),
                    status='scheduled'
                )
                db.session.add(shortlisted)
                shortlisted_count += 1
        
        db.session.commit()
        return jsonify({'message': f'Shortlisted {shortlisted_count} candidates'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/shortlisted/<int:job_id>')
def get_shortlisted(job_id):
    shortlisted = ShortlistedCandidate.query.filter_by(job_id=job_id).all()
    return jsonify([{
        'id': s.id,
        'candidate_name': s.get_candidate_name(),
        'interview_date': s.interview_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': s.status
    } for s in shortlisted])

@main.route('/api/candidate/<int:candidate_id>')
def get_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    return jsonify({
        'id': candidate.id,
        'name': candidate.name,
        'cv_text': candidate.cv_text,
        'match_score': candidate.match_score,
        'status': candidate.status,
        'is_shortlisted': candidate.is_shortlisted(),
        'interview_date': candidate.get_interview_date().strftime('%Y-%m-%d %H:%M:%S') if candidate.get_interview_date() else None
    }) 