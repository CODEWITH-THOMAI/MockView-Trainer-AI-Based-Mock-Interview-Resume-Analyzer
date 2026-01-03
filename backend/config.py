"""
Configuration file for MockView Trainer Backend
Manages environment variables and application settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # Frontend URL for CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    
    # Firebase configuration
    FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
    FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL', '')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour in seconds
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'docx', 'txt'}
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # ML Model settings
    NLTK_DATA_PATH = os.getenv('NLTK_DATA_PATH', 'nltk_data')
    SPACY_MODEL = os.getenv('SPACY_MODEL', 'en_core_web_sm')
    
    # API Rate limiting (optional)
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'false').lower() == 'true'
    RATELIMIT_DEFAULT = "100 per hour"
    
    # Scoring weights for AI evaluation
    INTERVIEW_WEIGHTS = {
        'relevance': 0.35,
        'grammar': 0.20,
        'completeness': 0.25,
        'sentiment': 0.20
    }
    
    FLUENCY_WEIGHTS = {
        'wpm': 0.25,
        'pause_frequency': 0.20,
        'filler_words': 0.25,
        'grammar': 0.30
    }
    
    RESUME_WEIGHTS = {
        'grammar': 0.25,
        'structure': 0.20,
        'ats_compatibility': 0.25,
        'keywords': 0.30
    }

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get the current configuration based on FLASK_ENV"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
