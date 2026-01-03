"""
Interview Routes
Handles mock interview sessions, questions, and answer evaluation
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

from routes.auth_routes import require_auth
from models.interview_session import InterviewSession
from services.question_generator_service import get_questions_for_role, generate_follow_up_question
from services.ai_interview_service import evaluate_interview_answer

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/start', methods=['POST'])
@require_auth
def start_interview():
    """
    Start a new interview session
    Generates questions based on job role and skill level
    """
    try:
        data = request.get_json()
        
        job_role = data.get('job_role', 'Software Engineer')
        skill_level = data.get('skill_level', 'Beginner')
        num_questions = data.get('num_questions', 5)
        interview_type = data.get('interview_type', 'text')
        
        # Validate inputs
        if num_questions < 1 or num_questions > 10:
            num_questions = 5
        
        # Generate questions
        questions = get_questions_for_role(job_role, skill_level, num_questions)
        
        # Create interview session
        session = InterviewSession.create(
            user_id=request.user_id,
            job_role=job_role,
            skill_level=skill_level,
            questions=questions,
            interview_type=interview_type
        )
        
        if session:
            return jsonify({
                'success': True,
                'message': 'Interview session started',
                'data': {
                    'session_id': session['id'],
                    'job_role': job_role,
                    'skill_level': skill_level,
                    'questions': questions,
                    'total_questions': len(questions)
                }
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create session'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to start interview',
            'error': str(e)
        }), 500

@interview_bp.route('/questions', methods=['GET'])
@require_auth
def get_questions():
    """
    Get interview questions (for standalone use without session)
    """
    try:
        job_role = request.args.get('job_role', 'Software Engineer')
        skill_level = request.args.get('skill_level', 'Beginner')
        count = int(request.args.get('count', 5))
        
        questions = get_questions_for_role(job_role, skill_level, count)
        
        return jsonify({
            'success': True,
            'data': {
                'questions': questions,
                'job_role': job_role,
                'skill_level': skill_level
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get questions',
            'error': str(e)
        }), 500

@interview_bp.route('/submit-answer', methods=['POST'])
@require_auth
def submit_answer():
    """
    Submit an answer for evaluation
    Provides AI-powered feedback and scoring
    """
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        answer = data.get('answer', '').strip()
        question_text = data.get('question')
        
        if not session_id or not question_id or not answer or not question_text:
            return jsonify({
                'success': False,
                'message': 'session_id, question_id, question, and answer are required'
            }), 400
        
        # Get session
        session = InterviewSession.get_by_id(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'message': 'Interview session not found'
            }), 404
        
        # Verify session belongs to user
        if session['user_id'] != request.user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized access to session'
            }), 403
        
        # Evaluate answer using AI
        evaluation = evaluate_interview_answer(
            question=question_text,
            answer=answer,
            job_role=session['job_role'],
            skill_level=session['skill_level']
        )
        
        # Create answer record
        answer_record = {
            'question_id': question_id,
            'question': question_text,
            'answer': answer,
            'evaluation': evaluation,
            'timestamp': datetime.now().isoformat()
        }
        
        # Update session with answer
        answers = session.get('answers', [])
        answers.append(answer_record)
        
        # Update scores
        scores = session.get('scores', {})
        scores[question_id] = {
            'score': evaluation['overall_score'],
            'relevance': evaluation['relevance']['score'],
            'grammar': evaluation['grammar']['score'],
            'completeness': evaluation['completeness']['score'],
            'sentiment': evaluation['sentiment_score']
        }
        
        InterviewSession.update(session_id, {
            'answers': answers,
            'scores': scores
        })
        
        return jsonify({
            'success': True,
            'message': 'Answer submitted and evaluated',
            'data': {
                'evaluation': evaluation,
                'question_id': question_id
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to submit answer',
            'error': str(e)
        }), 500

@interview_bp.route('/voice-answer', methods=['POST'])
@require_auth
def submit_voice_answer():
    """
    Submit a voice-based answer (with transcript)
    Similar to text answer but handles voice input
    """
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        transcript = data.get('transcript', '').strip()
        question_text = data.get('question')
        audio_duration = data.get('audio_duration', 0)
        
        if not session_id or not question_id or not transcript or not question_text:
            return jsonify({
                'success': False,
                'message': 'session_id, question_id, question, and transcript are required'
            }), 400
        
        # Get session
        session = InterviewSession.get_by_id(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'message': 'Interview session not found'
            }), 404
        
        if session['user_id'] != request.user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized access to session'
            }), 403
        
        # Evaluate transcript
        evaluation = evaluate_interview_answer(
            question=question_text,
            answer=transcript,
            job_role=session['job_role'],
            skill_level=session['skill_level']
        )
        
        # Create answer record
        answer_record = {
            'question_id': question_id,
            'question': question_text,
            'answer': transcript,
            'is_voice': True,
            'audio_duration': audio_duration,
            'evaluation': evaluation,
            'timestamp': datetime.now().isoformat()
        }
        
        # Update session
        answers = session.get('answers', [])
        answers.append(answer_record)
        
        scores = session.get('scores', {})
        scores[question_id] = {
            'score': evaluation['overall_score'],
            'relevance': evaluation['relevance']['score'],
            'grammar': evaluation['grammar']['score'],
            'completeness': evaluation['completeness']['score'],
            'sentiment': evaluation['sentiment_score']
        }
        
        InterviewSession.update(session_id, {
            'answers': answers,
            'scores': scores
        })
        
        return jsonify({
            'success': True,
            'message': 'Voice answer submitted and evaluated',
            'data': {
                'evaluation': evaluation,
                'question_id': question_id
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to submit voice answer',
            'error': str(e)
        }), 500

@interview_bp.route('/feedback/<session_id>', methods=['GET'])
@require_auth
def get_feedback(session_id):
    """
    Get complete feedback for an interview session
    Includes overall score, individual scores, and recommendations
    """
    try:
        # Get session
        session = InterviewSession.get_by_id(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'message': 'Interview session not found'
            }), 404
        
        # Verify ownership
        if session['user_id'] != request.user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized access to session'
            }), 403
        
        # Calculate overall session score
        scores = session.get('scores', {})
        if scores:
            score_values = [s['score'] for s in scores.values()]
            overall_score = sum(score_values) / len(score_values)
        else:
            overall_score = 0
        
        # Mark session as completed
        InterviewSession.update(session_id, {
            'status': 'completed',
            'overall_score': int(overall_score),
            'completed_at': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'data': {
                'session_id': session_id,
                'job_role': session['job_role'],
                'skill_level': session['skill_level'],
                'overall_score': round(overall_score, 2),
                'scores': scores,
                'answers': session.get('answers', []),
                'questions': session.get('questions', []),
                'created_at': session.get('created_at')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get feedback',
            'error': str(e)
        }), 500
