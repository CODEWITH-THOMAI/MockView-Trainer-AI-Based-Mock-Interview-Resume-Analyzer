"""
Validation Utilities
Input validation functions for various data types
"""

import re
from typing import Tuple

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength
    Password must be at least 8 characters and contain:
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Args:
        password: Password to validate
        
    Returns:
        tuple: (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is valid"

def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """
    Validate file extension
    
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions (e.g., {'pdf', 'docx'})
        
    Returns:
        bool: True if extension is allowed
    """
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions

def validate_skill_level(skill_level: str) -> bool:
    """
    Validate skill level
    
    Args:
        skill_level: Skill level to validate
        
    Returns:
        bool: True if valid skill level
    """
    valid_levels = {'Beginner', 'Intermediate', 'Advanced'}
    return skill_level in valid_levels

def validate_job_role(job_role: str) -> bool:
    """
    Validate job role
    
    Args:
        job_role: Job role to validate
        
    Returns:
        bool: True if valid job role
    """
    valid_roles = {
        'Software Engineer',
        'Data Scientist',
        'Product Manager',
        'DevOps Engineer',
        'Frontend Developer',
        'Backend Developer',
        'Full Stack Developer',
        'Mobile Developer',
        'QA Engineer',
        'UI/UX Designer'
    }
    return job_role in valid_roles

def sanitize_string(text: str, max_length: int = 1000) -> str:
    """
    Sanitize string input by removing potentially harmful characters
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove null bytes and control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Truncate to max length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()
