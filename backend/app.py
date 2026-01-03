"""
MockView Trainer - Main Flask Application
AI-Based Mock Interview & Resume Analyzer Backend
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from routes.auth_routes import auth_bp
from routes.interview_routes import interview_bp
from routes.fluency_routes import fluency_bp
from routes.resume_routes import resume_bp
from routes.dashboard_routes import dashboard_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload
    
    # Enable CORS for frontend connection
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('FRONTEND_URL', 'http://localhost:5173'),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints (API routes)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(interview_bp, url_prefix='/api/interview')
    app.register_blueprint(fluency_bp, url_prefix='/api/fluency')
    app.register_blueprint(resume_bp, url_prefix='/api/resume')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'MockView Trainer API is running',
            'version': '1.0.0'
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({
            'success': True,
            'status': 'healthy'
        })
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'error': str(error)
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(error)
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad request',
            'error': str(error)
        }), 400
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"Starting MockView Trainer API on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
