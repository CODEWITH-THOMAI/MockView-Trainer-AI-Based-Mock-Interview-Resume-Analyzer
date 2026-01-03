"""
Dashboard Routes
Provides user analytics, statistics, and session history
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

from routes.auth_routes import require_auth
from database.firebase_config import (
    get_firestore_client,
    INTERVIEW_SESSIONS_COLLECTION,
    FLUENCY_TESTS_COLLECTION,
    RESUMES_COLLECTION
)

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@require_auth
def get_stats():
    """
    Get user statistics and analytics
    Returns counts, averages, and trends
    """
    try:
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        user_id = request.user_id
        
        # Get interview sessions
        interview_sessions = db.collection(INTERVIEW_SESSIONS_COLLECTION)\
            .where('user_id', '==', user_id)\
            .get()
        
        interview_count = len(interview_sessions)
        interview_scores = []
        
        for session in interview_sessions:
            session_data = session.to_dict()
            score = session_data.get('overall_score', 0)
            if score > 0:
                interview_scores.append(score)
        
        avg_interview_score = sum(interview_scores) / len(interview_scores) if interview_scores else 0
        
        # Get fluency tests
        fluency_tests = db.collection(FLUENCY_TESTS_COLLECTION)\
            .where('user_id', '==', user_id)\
            .get()
        
        fluency_count = len(fluency_tests)
        fluency_scores = []
        
        for test in fluency_tests:
            test_data = test.to_dict()
            score = test_data.get('fluency_score', 0)
            if score > 0:
                fluency_scores.append(score)
        
        latest_fluency_score = fluency_scores[-1] if fluency_scores else 0
        avg_fluency_score = sum(fluency_scores) / len(fluency_scores) if fluency_scores else 0
        
        # Get resumes
        resumes = db.collection(RESUMES_COLLECTION)\
            .where('user_id', '==', user_id)\
            .get()
        
        resume_count = len(resumes)
        resume_scores = []
        
        for resume in resumes:
            resume_data = resume.to_dict()
            score = resume_data.get('score', 0)
            if score > 0:
                resume_scores.append(score)
        
        latest_resume_score = resume_scores[-1] if resume_scores else 0
        
        return jsonify({
            'success': True,
            'data': {
                'interviews': {
                    'total_count': interview_count,
                    'average_score': round(avg_interview_score, 2),
                    'latest_score': interview_scores[-1] if interview_scores else 0
                },
                'fluency_tests': {
                    'total_count': fluency_count,
                    'average_score': round(avg_fluency_score, 2),
                    'latest_score': latest_fluency_score
                },
                'resumes': {
                    'total_count': resume_count,
                    'latest_score': latest_resume_score
                },
                'overall': {
                    'total_activities': interview_count + fluency_count + resume_count,
                    'overall_performance': round((avg_interview_score + avg_fluency_score + latest_resume_score) / 3, 2) if (interview_count + fluency_count + resume_count) > 0 else 0
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get statistics',
            'error': str(e)
        }), 500

@dashboard_bp.route('/history', methods=['GET'])
@require_auth
def get_history():
    """
    Get user session history
    Returns recent interviews, fluency tests, and resumes
    """
    try:
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        user_id = request.user_id
        limit = int(request.args.get('limit', 10))
        
        history = []
        
        # Get recent interview sessions
        interview_sessions = db.collection(INTERVIEW_SESSIONS_COLLECTION)\
            .where('user_id', '==', user_id)\
            .order_by('timestamp', direction='DESCENDING')\
            .limit(limit)\
            .get()
        
        for session in interview_sessions:
            session_data = session.to_dict()
            history.append({
                'id': session_data.get('session_id'),
                'type': 'interview',
                'title': f"{session_data.get('job_role')} Interview - {session_data.get('skill_level')}",
                'score': session_data.get('overall_score', 0),
                'status': session_data.get('status', 'completed'),
                'timestamp': session_data.get('timestamp'),
                'details': {
                    'job_role': session_data.get('job_role'),
                    'skill_level': session_data.get('skill_level'),
                    'questions_count': len(session_data.get('questions', []))
                }
            })
        
        # Get recent fluency tests
        fluency_tests = db.collection(FLUENCY_TESTS_COLLECTION)\
            .where('user_id', '==', user_id)\
            .order_by('timestamp', direction='DESCENDING')\
            .limit(limit)\
            .get()
        
        for test in fluency_tests:
            test_data = test.to_dict()
            history.append({
                'id': test_data.get('test_id'),
                'type': 'fluency',
                'title': 'English Fluency Test',
                'score': test_data.get('fluency_score', 0),
                'status': 'completed',
                'timestamp': test_data.get('timestamp'),
                'details': {
                    'wpm': test_data.get('wpm', 0),
                    'filler_word_count': test_data.get('filler_word_count', 0)
                }
            })
        
        # Get recent resumes
        resumes = db.collection(RESUMES_COLLECTION)\
            .where('user_id', '==', user_id)\
            .order_by('timestamp', direction='DESCENDING')\
            .limit(limit)\
            .get()
        
        for resume in resumes:
            resume_data = resume.to_dict()
            history.append({
                'id': resume_data.get('resume_id'),
                'type': 'resume',
                'title': 'Resume Analysis',
                'score': resume_data.get('score', 0),
                'status': 'completed',
                'timestamp': resume_data.get('timestamp'),
                'details': {
                    'suggestions_count': len(resume_data.get('suggestions', []))
                }
            })
        
        # Sort by timestamp (most recent first)
        history.sort(key=lambda x: x['timestamp'] if x['timestamp'] else datetime.min, reverse=True)
        
        # Limit results
        history = history[:limit]
        
        return jsonify({
            'success': True,
            'data': {
                'history': history,
                'total': len(history)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get history',
            'error': str(e)
        }), 500

@dashboard_bp.route('/trends', methods=['GET'])
@require_auth
def get_trends():
    """
    Get performance trends over time
    Returns score trends for the past 30 days
    """
    try:
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        user_id = request.user_id
        days = int(request.args.get('days', 30))
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get interview sessions in date range
        interview_sessions = db.collection(INTERVIEW_SESSIONS_COLLECTION)\
            .where('user_id', '==', user_id)\
            .where('timestamp', '>=', start_date)\
            .where('timestamp', '<=', end_date)\
            .order_by('timestamp')\
            .get()
        
        interview_trend = []
        for session in interview_sessions:
            session_data = session.to_dict()
            interview_trend.append({
                'date': session_data.get('timestamp'),
                'score': session_data.get('overall_score', 0)
            })
        
        # Get fluency tests in date range
        fluency_tests = db.collection(FLUENCY_TESTS_COLLECTION)\
            .where('user_id', '==', user_id)\
            .where('timestamp', '>=', start_date)\
            .where('timestamp', '<=', end_date)\
            .order_by('timestamp')\
            .get()
        
        fluency_trend = []
        for test in fluency_tests:
            test_data = test.to_dict()
            fluency_trend.append({
                'date': test_data.get('timestamp'),
                'score': test_data.get('fluency_score', 0)
            })
        
        return jsonify({
            'success': True,
            'data': {
                'date_range': {
                    'start': start_date,
                    'end': end_date,
                    'days': days
                },
                'trends': {
                    'interviews': interview_trend,
                    'fluency': fluency_trend
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get trends',
            'error': str(e)
        }), 500
