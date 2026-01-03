"""
Firebase Configuration and Initialization
Sets up Firebase Admin SDK for Authentication, Firestore, and Storage
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from config import Config

# Global Firebase instances
db = None
firebase_app = None

def initialize_firebase():
    """
    Initialize Firebase Admin SDK
    Returns: tuple (firestore_client, firebase_app)
    """
    global db, firebase_app
    
    try:
        # Check if Firebase is already initialized
        if firebase_app is not None:
            print("Firebase already initialized")
            return db, firebase_app
        
        # Get credentials path from config
        cred_path = Config.FIREBASE_CREDENTIALS_PATH
        
        # Check if credentials file exists
        if not os.path.exists(cred_path):
            print(f"Warning: Firebase credentials file not found at {cred_path}")
            print("Firebase features will be disabled. Please add firebase-credentials.json")
            return None, None
        
        # Initialize Firebase with credentials
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': Config.FIREBASE_DATABASE_URL,
            'storageBucket': f"{cred.project_id}.appspot.com"
        })
        
        # Get Firestore client
        db = firestore.client()
        
        print("Firebase initialized successfully")
        print(f"Project ID: {cred.project_id}")
        
        return db, firebase_app
        
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        return None, None

def get_firestore_client():
    """Get or initialize Firestore client"""
    global db
    if db is None:
        db, _ = initialize_firebase()
    return db

def test_firebase_connection():
    """
    Test Firebase connection
    Returns: dict with connection status
    """
    try:
        db = get_firestore_client()
        
        if db is None:
            return {
                'success': False,
                'message': 'Firebase not initialized',
                'firestore': False,
                'auth': False,
                'storage': False
            }
        
        # Test Firestore
        firestore_working = False
        try:
            # Try to access a test collection
            test_ref = db.collection('_test_connection')
            firestore_working = True
        except Exception as e:
            print(f"Firestore test failed: {str(e)}")
        
        # Test Auth
        auth_working = False
        try:
            # Try to list users (will work even if no users exist)
            auth.list_users(max_results=1)
            auth_working = True
        except Exception as e:
            print(f"Auth test failed: {str(e)}")
        
        # Test Storage
        storage_working = False
        try:
            bucket = storage.bucket()
            storage_working = bucket is not None
        except Exception as e:
            print(f"Storage test failed: {str(e)}")
        
        return {
            'success': True,
            'message': 'Firebase connection tested',
            'firestore': firestore_working,
            'auth': auth_working,
            'storage': storage_working
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Firebase connection test failed: {str(e)}',
            'firestore': False,
            'auth': False,
            'storage': False
        }

# Collection names constants
USERS_COLLECTION = 'users'
INTERVIEW_SESSIONS_COLLECTION = 'interview_sessions'
FLUENCY_TESTS_COLLECTION = 'fluency_tests'
RESUMES_COLLECTION = 'resumes'
