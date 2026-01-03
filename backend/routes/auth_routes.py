"""
Authentication Routes
Handles user signup, login, and profile management with Supabase Auth
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from functools import wraps

from database.supabase_config import get_supabase_client
from models.user import User
from utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': 'No authorization token provided'
            }), 401
        
        token = auth_header.replace('Bearer ', '')
        
        try:
            supabase = get_supabase_client()
            if supabase is None:
                return jsonify({
                    'success': False,
                    'message': 'Database not available'
                }), 503
            
            # Verify token with Supabase
            user_response = supabase.auth.get_user(token)
            
            if user_response and user_response.user:
                request.user_id = user_response.user.id
                request.user_email = user_response.user.email
                return f(*args, **kwargs)
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid token'
                }), 401
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Authentication failed: {str(e)}'
            }), 401
    
    return decorated_function

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User registration with Supabase Auth
    Body: { email, password, name, skill_level, job_role }
    """
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        skill_level = data.get('skill_level', 'Beginner')
        job_role = data.get('job_role', 'Software Engineer')
        
        # Validate input
        if not all([email, password, name]):
            return jsonify({
                'success': False,
                'message': 'Email, password, and name are required'
            }), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Validate password strength
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        supabase = get_supabase_client()
        if supabase is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Create auth user in Supabase
        auth_response = supabase.auth.sign_up({
            'email': email,
            'password': password
        })
        
        if auth_response.user:
            # Create user profile in database
            user = User.create(
                email=email,
                name=name,
                skill_level=skill_level,
                job_role=job_role,
                user_id=auth_response.user.id
            )
            
            session_data = None
            access_token = None
            
            if auth_response.session:
                session_data = {
                    'access_token': auth_response.session.access_token,
                    'refresh_token': auth_response.session.refresh_token,
                    'expires_at': auth_response.session.expires_at,
                    'token_type': auth_response.session.token_type
                }
                access_token = auth_response.session.access_token
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'data': {
                    'user': user,
                    'session': session_data,
                    'access_token': access_token
                }
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Registration failed'
            }), 400
            
    except Exception as e:
        error_msg = str(e)
        # Handle common Supabase errors
        if 'User already registered' in error_msg or 'email' in error_msg.lower():
            return jsonify({
                'success': False,
                'message': 'Email already exists'
            }), 400
        
        return jsonify({
            'success': False,
            'message': f'Error: {error_msg}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login with Supabase Auth
    Body: { email, password }
    """
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not all([email, password]):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        supabase = get_supabase_client()
        if supabase is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Sign in with Supabase
        auth_response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if auth_response.user:
            # Get user profile
            user = User.get_by_email(email)
            
            session_data = None
            access_token = None
            
            if auth_response.session:
                session_data = {
                    'access_token': auth_response.session.access_token,
                    'refresh_token': auth_response.session.refresh_token,
                    'expires_at': auth_response.session.expires_at,
                    'token_type': auth_response.session.token_type
                }
                access_token = auth_response.session.access_token
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'data': {
                    'user': user,
                    'session': session_data,
                    'access_token': access_token
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get user profile (requires auth token)"""
    try:
        user = User.get_by_email(request.user_email)
        
        if user:
            return jsonify({
                'success': True,
                'data': user
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'User profile not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        
        # Get current user
        user = User.get_by_email(request.user_email)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Update allowed fields
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'skill_level' in data:
            update_data['skill_level'] = data['skill_level']
        if 'job_role' in data:
            update_data['job_role'] = data['job_role']
        
        if update_data:
            updated_user = User.update(user['id'], update_data)
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'data': updated_user
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No valid fields to update'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user (invalidate session)"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Sign out from Supabase
        supabase.auth.sign_out()
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500
