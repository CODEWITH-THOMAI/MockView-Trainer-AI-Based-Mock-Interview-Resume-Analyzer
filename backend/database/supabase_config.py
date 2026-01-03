"""
Supabase Configuration and Initialization
Sets up Supabase client for PostgreSQL database, Authentication, and Storage
"""

from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

# Initialize Supabase client
supabase: Client = None

def initialize_supabase():
    """
    Initialize Supabase client
    Returns: Supabase client instance
    """
    global supabase
    
    try:
        if supabase is not None:
            print("Supabase already initialized")
            return supabase
        
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("Warning: Supabase credentials not found in environment")
            print("Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env file")
            return None
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase initialized successfully")
        print(f"Connected to: {SUPABASE_URL}")
        
        return supabase
        
    except Exception as e:
        print(f"Error initializing Supabase: {str(e)}")
        return None

def get_supabase_client():
    """
    Returns initialized Supabase client
    Usage: db = get_supabase_client()
    """
    global supabase
    if supabase is None:
        supabase = initialize_supabase()
    return supabase

def test_connection():
    """
    Test Supabase connection
    Returns True if successful, False otherwise
    """
    try:
        client = get_supabase_client()
        if client is None:
            print("✗ Supabase client not initialized")
            return False
        
        # Test query - try to select from users table
        result = client.table('users').select('*').limit(1).execute()
        print("✓ Supabase connected successfully")
        return True
    except Exception as e:
        print(f"✗ Supabase connection failed: {str(e)}")
        return False

# Table names constants
USERS_TABLE = 'users'
INTERVIEW_SESSIONS_TABLE = 'interview_sessions'
FLUENCY_TESTS_TABLE = 'fluency_tests'
RESUMES_TABLE = 'resumes'
CHAT_HISTORY_TABLE = 'chat_history'
