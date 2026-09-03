"""
Configuration file for AI Resume Scanner
Modify these settings as needed for your environment
"""

import os

class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
    
    # Database Configuration
    DATABASE_FILE = os.environ.get('DATABASE_FILE') or 'resume_database.json'
    
    # AI Analysis Configuration
    MAX_TEXT_LENGTH = 10000  # Maximum text length to store in database
    SKILL_CATEGORIES = {
        'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin'],
        'web_technologies': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express'],
        'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'sqlite'],
        'cloud_platforms': ['aws', 'azure', 'google cloud', 'heroku', 'digitalocean'],
        'tools': ['git', 'docker', 'kubernetes', 'jenkins', 'jira', 'confluence', 'slack'],
        'frameworks': ['tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib']
    }
    
    # Experience level indicators
    EXPERIENCE_INDICATORS = {
        'entry': ['entry level', 'junior', '0-2 years', '1-2 years', 'fresher', 'graduate'],
        'mid': ['mid level', 'intermediate', '3-5 years', '4-6 years', 'experienced'],
        'senior': ['senior', 'lead', 'principal', '5+ years', '7+ years', '10+ years', 'expert']
    }
    
    # Scoring weights (must sum to 1.0)
    SCORING_WEIGHTS = {
        'skills': 0.4,      # 40% weight for skills
        'experience': 0.3,  # 30% weight for experience level
        'education': 0.2,   # 20% weight for education
        'readability': 0.1  # 10% weight for readability
    }
    
    # Server Configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Security Configuration
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE') or 'app.log'
    
    # Performance Configuration
    MAX_RESUMES_PER_PAGE = int(os.environ.get('MAX_RESUMES_PER_PAGE', 50))
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', 300))  # 5 minutes
    
    # Export Configuration
    EXPORT_FORMATS = ['json', 'csv']
    MAX_EXPORT_SIZE = int(os.environ.get('MAX_EXPORT_SIZE', 1000))  # Max resumes to export

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_FILE = 'test_database.json'
    UPLOAD_FOLDER = 'test_uploads'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration object by name."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])




