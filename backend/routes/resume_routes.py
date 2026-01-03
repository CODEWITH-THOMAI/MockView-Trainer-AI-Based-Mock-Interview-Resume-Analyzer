"""
Resume Routes
Handles resume building, analysis, and export
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

from routes.auth_routes import require_auth
from database.firebase_config import get_firestore_client, RESUMES_COLLECTION
from models.resume import Resume

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/build', methods=['POST'])
@require_auth
def build_resume():
    """
    Build resume from form data
    Saves resume content to database
    """
    try:
        data = request.get_json()
        
        # Extract resume content
        content = {
            'personal_info': data.get('personal_info', {}),
            'education': data.get('education', []),
            'experience': data.get('experience', []),
            'skills': data.get('skills', []),
            'certifications': data.get('certifications', []),
            'projects': data.get('projects', [])
        }
        
        # Create resume
        resume = Resume(
            user_id=request.user_id,
            content=content
        )
        
        # Save to Firestore
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        db.collection(RESUMES_COLLECTION).document(resume.resume_id).set(resume.to_dict())
        
        return jsonify({
            'success': True,
            'message': 'Resume created successfully',
            'data': {
                'resume_id': resume.resume_id,
                'content': content
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to build resume',
            'error': str(e)
        }), 500

@resume_bp.route('/analyze', methods=['POST'])
@require_auth
def analyze_resume():
    """
    Analyze uploaded resume
    Provides feedback and scoring
    """
    try:
        data = request.get_json()
        
        resume_text = data.get('resume_text', '').strip()
        job_role = data.get('job_role', 'Software Engineer')
        
        if not resume_text:
            return jsonify({
                'success': False,
                'message': 'resume_text is required'
            }), 400
        
        # Perform basic analysis (simplified version)
        # In production, this would use advanced NLP and ATS compatibility checks
        
        from ml_models.nlp_processor import (
            count_words, count_sentences, extract_keywords, detect_grammar_errors_simple
        )
        
        word_count = count_words(resume_text)
        sentence_count = count_sentences(resume_text)
        keywords = extract_keywords(resume_text, top_n=15)
        grammar_errors = detect_grammar_errors_simple(resume_text)
        
        # Calculate scores
        grammar_score = max(0, 100 - (len(grammar_errors) * 5))
        
        # Structure score (based on word count and sentence count)
        if word_count >= 200 and sentence_count >= 10:
            structure_score = 90
        elif word_count >= 150:
            structure_score = 75
        elif word_count >= 100:
            structure_score = 60
        else:
            structure_score = 40
        
        # ATS compatibility score (simplified)
        ats_score = 80  # Base score
        if len(keywords) < 5:
            ats_score -= 20
        
        # Keyword score (job-specific keywords)
        from services.ai_interview_service import load_job_keywords
        job_keywords = load_job_keywords().get(job_role, [])
        
        matched_keywords = 0
        for keyword in keywords:
            for job_keyword in job_keywords:
                if keyword.lower() in job_keyword.lower():
                    matched_keywords += 1
                    break
        
        keyword_score = min(100, (matched_keywords / max(len(keywords), 1)) * 100)
        
        # Calculate overall score
        analysis = {
            'grammar_score': grammar_score,
            'structure_score': structure_score,
            'ats_score': ats_score,
            'keyword_score': keyword_score,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'keywords_found': keywords,
            'matched_keywords': matched_keywords,
            'grammar_errors': grammar_errors
        }
        
        # Create resume object
        resume = Resume(
            user_id=request.user_id,
            content={'text': resume_text, 'job_role': job_role},
            analysis=analysis
        )
        
        # Calculate overall score
        overall_score = resume.calculate_score()
        
        # Generate suggestions
        suggestions = generate_resume_suggestions(analysis, job_role)
        resume.suggestions = suggestions
        
        # Save to Firestore
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        db.collection(RESUMES_COLLECTION).document(resume.resume_id).set(resume.to_dict())
        
        return jsonify({
            'success': True,
            'message': 'Resume analyzed successfully',
            'data': {
                'resume_id': resume.resume_id,
                'overall_score': overall_score,
                'analysis': analysis,
                'suggestions': suggestions
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to analyze resume',
            'error': str(e)
        }), 500

@resume_bp.route('/templates', methods=['GET'])
@require_auth
def get_templates():
    """
    Get available resume templates
    """
    templates = [
        {
            'id': 'modern',
            'name': 'Modern Professional',
            'description': 'Clean and modern design suitable for tech roles',
            'preview_url': '/templates/modern.png'
        },
        {
            'id': 'classic',
            'name': 'Classic ATS',
            'description': 'ATS-friendly format with traditional layout',
            'preview_url': '/templates/classic.png'
        },
        {
            'id': 'creative',
            'name': 'Creative Designer',
            'description': 'Eye-catching design for creative professionals',
            'preview_url': '/templates/creative.png'
        }
    ]
    
    return jsonify({
        'success': True,
        'data': {
            'templates': templates
        }
    }), 200

@resume_bp.route('/export', methods=['POST'])
@require_auth
def export_resume():
    """
    Export resume as PDF
    Note: This is a placeholder. Actual PDF generation would require additional libraries
    """
    try:
        data = request.get_json()
        
        resume_id = data.get('resume_id')
        template_id = data.get('template', 'modern')
        
        if not resume_id:
            return jsonify({
                'success': False,
                'message': 'resume_id is required'
            }), 400
        
        # In production, generate PDF here using libraries like ReportLab or WeasyPrint
        # For now, return a success message
        
        return jsonify({
            'success': True,
            'message': 'Resume export initiated',
            'data': {
                'resume_id': resume_id,
                'template': template_id,
                'download_url': f'/downloads/resume_{resume_id}.pdf'
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to export resume',
            'error': str(e)
        }), 500

@resume_bp.route('/feedback/<resume_id>', methods=['GET'])
@require_auth
def get_resume_feedback(resume_id):
    """
    Get detailed resume feedback and suggestions
    """
    try:
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Get resume
        resume_doc = db.collection(RESUMES_COLLECTION).document(resume_id).get()
        
        if not resume_doc.exists:
            return jsonify({
                'success': False,
                'message': 'Resume not found'
            }), 404
        
        resume_data = resume_doc.to_dict()
        
        # Verify ownership
        if resume_data['user_id'] != request.user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized access to resume'
            }), 403
        
        return jsonify({
            'success': True,
            'data': {
                'resume_id': resume_id,
                'score': resume_data.get('score', 0),
                'analysis': resume_data.get('analysis', {}),
                'suggestions': resume_data.get('suggestions', []),
                'timestamp': resume_data.get('timestamp')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get resume feedback',
            'error': str(e)
        }), 500

def generate_resume_suggestions(analysis: dict, job_role: str) -> list:
    """Generate improvement suggestions based on analysis"""
    suggestions = []
    
    if analysis['grammar_score'] < 80:
        suggestions.append("Review grammar and spelling. Consider using a grammar checker.")
    
    if analysis['structure_score'] < 70:
        suggestions.append("Expand your resume with more details about your experience and achievements.")
    
    if analysis['keyword_score'] < 60:
        suggestions.append(f"Add more {job_role}-specific keywords and technical skills.")
    
    if analysis['ats_score'] < 75:
        suggestions.append("Use standard section headings (Experience, Education, Skills) for better ATS compatibility.")
    
    if analysis['word_count'] < 200:
        suggestions.append("Your resume is too brief. Add more details about your accomplishments.")
    
    if analysis['matched_keywords'] < 5:
        suggestions.append("Include more industry-relevant keywords to pass ATS screening.")
    
    suggestions.append("Use action verbs to describe your achievements (e.g., 'Developed', 'Implemented', 'Led').")
    suggestions.append("Quantify your achievements with numbers and metrics where possible.")
    
    return suggestions
