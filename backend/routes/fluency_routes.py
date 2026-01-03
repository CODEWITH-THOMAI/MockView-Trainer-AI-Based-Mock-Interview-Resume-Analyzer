"""
Fluency Routes
Handles fluency testing and speech analysis
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

from routes.auth_routes import require_auth
from database.firebase_config import get_firestore_client, FLUENCY_TESTS_COLLECTION
from models.fluency_test import FluencyTest
from ml_models.fluency_scorer import analyze_speech_fluency

fluency_bp = Blueprint('fluency', __name__)

@fluency_bp.route('/test', methods=['POST'])
@require_auth
def start_fluency_test():
    """
    Start a new fluency test
    """
    try:
        # Create new fluency test
        test = FluencyTest(user_id=request.user_id)
        
        # Save to Firestore
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        db.collection(FLUENCY_TESTS_COLLECTION).document(test.test_id).set(test.to_dict())
        
        return jsonify({
            'success': True,
            'message': 'Fluency test started',
            'data': {
                'test_id': test.test_id
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to start fluency test',
            'error': str(e)
        }), 500

@fluency_bp.route('/analyze', methods=['POST'])
@require_auth
def analyze_fluency():
    """
    Analyze speech fluency from transcript
    Provides detailed analysis and scoring
    """
    try:
        data = request.get_json()
        
        test_id = data.get('test_id')
        transcript = data.get('transcript', '').strip()
        audio_duration = data.get('audio_duration', 0)
        
        if not test_id or not transcript:
            return jsonify({
                'success': False,
                'message': 'test_id and transcript are required'
            }), 400
        
        # Analyze fluency
        analysis = analyze_speech_fluency(transcript, audio_duration)
        
        # Get Firestore client
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Get test document
        test_ref = db.collection(FLUENCY_TESTS_COLLECTION).document(test_id)
        test_doc = test_ref.get()
        
        if not test_doc.exists:
            return jsonify({
                'success': False,
                'message': 'Fluency test not found'
            }), 404
        
        test_data = test_doc.to_dict()
        
        # Verify ownership
        if test_data['user_id'] != request.user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized access to test'
            }), 403
        
        # Update test with analysis results
        test_ref.update({
            'transcript': transcript,
            'audio_duration': audio_duration,
            'fluency_score': analysis['fluency_score'],
            'pronunciation_score': 85.0,  # Placeholder - needs audio analysis
            'grammar_score': 100 - (len(analysis['grammar_errors']) * 5),
            'wpm': analysis['wpm'],
            'pause_count': analysis['pauses']['count'],
            'filler_word_count': analysis['filler_words']['total_count'],
            'feedback': analysis['feedback'],
            'detailed_analysis': {
                'filler_words': analysis['filler_words'],
                'pauses': analysis['pauses'],
                'grammar_errors': analysis['grammar_errors']
            }
        })
        
        # Get updated test
        updated_test = test_ref.get().to_dict()
        test_obj = FluencyTest.from_dict(updated_test)
        overall_score = test_obj.calculate_overall_score()
        
        return jsonify({
            'success': True,
            'message': 'Fluency analyzed successfully',
            'data': {
                'test_id': test_id,
                'overall_score': overall_score,
                'fluency_score': analysis['fluency_score'],
                'pronunciation_score': 85.0,
                'grammar_score': 100 - (len(analysis['grammar_errors']) * 5),
                'wpm': analysis['wpm'],
                'word_count': analysis['word_count'],
                'filler_word_count': analysis['filler_words']['total_count'],
                'pause_count': analysis['pauses']['count'],
                'feedback': analysis['feedback'],
                'detailed_analysis': analysis
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to analyze fluency',
            'error': str(e)
        }), 500

@fluency_bp.route('/score/<test_id>', methods=['GET'])
@require_auth
def get_fluency_score(test_id):
    """
    Get fluency test results by test ID
    """
    try:
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Get test
        test_doc = db.collection(FLUENCY_TESTS_COLLECTION).document(test_id).get()
        
        if not test_doc.exists:
            return jsonify({
                'success': False,
                'message': 'Fluency test not found'
            }), 404
        
        test_data = test_doc.to_dict()
        
        # Verify ownership
        if test_data['user_id'] != request.user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized access to test'
            }), 403
        
        # Calculate overall score
        test_obj = FluencyTest.from_dict(test_data)
        overall_score = test_obj.calculate_overall_score()
        
        return jsonify({
            'success': True,
            'data': {
                'test_id': test_id,
                'overall_score': overall_score,
                'fluency_score': test_data.get('fluency_score', 0),
                'pronunciation_score': test_data.get('pronunciation_score', 0),
                'grammar_score': test_data.get('grammar_score', 0),
                'wpm': test_data.get('wpm', 0),
                'filler_word_count': test_data.get('filler_word_count', 0),
                'pause_count': test_data.get('pause_count', 0),
                'feedback': test_data.get('feedback', []),
                'detailed_analysis': test_data.get('detailed_analysis', {}),
                'timestamp': test_data.get('timestamp')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get fluency score',
            'error': str(e)
        }), 500
