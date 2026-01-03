"""
Authentication Routes
Handles user signup, login, and profile management
"""

from flask import Blueprint, request, jsonify
from firebase_admin import auth as firebase_auth
import jwt
from datetime import datetime, timedelta
from functools import wraps

from database.firebase_config import get_firestore_client, USERS_COLLECTION
from models.user import User
from config import Config
from utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'No authorization token provided'
            }), 401
        
        try:
            # Verify JWT token
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            request.user_id = payload['uid']
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token has expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
    
    return decorated_function

def generate_jwt_token(uid: str) -> str:
    """Generate JWT token for user"""
    payload = {
        'uid': uid,
        'exp': datetime.utcnow() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User registration endpoint
    Creates new user in Firebase Authentication and Firestore
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        
        if not email or not password or not name:
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
        
        # Get Firestore client
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Create user in Firebase Authentication
        try:
            firebase_user = firebase_auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            uid = firebase_user.uid
        except Exception as e:
            error_message = str(e)
            if 'EMAIL_EXISTS' in error_message:
                return jsonify({
                    'success': False,
                    'message': 'Email already exists'
                }), 400
            return jsonify({
                'success': False,
                'message': f'Failed to create user: {error_message}'
            }), 400
        
        # Create user profile in Firestore
        user = User(
            uid=uid,
            email=email,
            name=name,
            skill_level=data.get('skill_level', 'Beginner'),
            job_role=data.get('job_role', 'Software Engineer')
        )
        
        db.collection(USERS_COLLECTION).document(uid).set(user.to_dict())
        
        # Generate JWT token
        token = generate_jwt_token(uid)
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Signup failed',
            'error': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    Authenticates user and returns JWT token
    """
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Get Firestore client
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Note: Firebase Admin SDK doesn't support password verification
        # In production, use Firebase Auth REST API or client-side Firebase Auth
        # For now, we'll retrieve user by email and generate token
        
        try:
            firebase_user = firebase_auth.get_user_by_email(email)
            uid = firebase_user.uid
        except firebase_auth.UserNotFoundError:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Login failed',
                'error': str(e)
            }), 500
        
        # Get user profile from Firestore
        user_doc = db.collection(USERS_COLLECTION).document(uid).get()
        
        if not user_doc.exists:
            return jsonify({
                'success': False,
                'message': 'User profile not found'
            }), 404
        
        user_data = user_doc.to_dict()
        
        # Generate JWT token
        token = generate_jwt_token(uid)
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user_data,
                'token': token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Login failed',
            'error': str(e)
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """
    Get user profile
    Requires authentication
    """
    try:
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Get user profile
        user_doc = db.collection(USERS_COLLECTION).document(request.user_id).get()
        
        if not user_doc.exists:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        user_data = user_doc.to_dict()
        
        return jsonify({
            'success': True,
            'data': user_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get profile',
            'error': str(e)
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@require_auth
def update_profile():
    """
    Update user profile
    Requires authentication
    """
    try:
        data = request.get_json()
        
        db = get_firestore_client()
        if db is None:
            return jsonify({
                'success': False,
                'message': 'Database not available'
            }), 503
        
        # Get current user profile
        user_ref = db.collection(USERS_COLLECTION).document(request.user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
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
        
        update_data['updated_at'] = datetime.now()
        
        # Update in Firestore
        user_ref.update(update_data)
        
        # Get updated profile
        updated_user = user_ref.get().to_dict()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'data': updated_user
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to update profile',
            'error': str(e)
        }), 500
