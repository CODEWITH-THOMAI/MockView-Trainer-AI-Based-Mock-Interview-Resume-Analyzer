"""
Question Generator Service
Generates interview questions based on job role and skill level
"""

import json
import random
import os
from typing import List, Dict

# Path to questions data file
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'interview_questions.json')

# Cache for questions
_questions_cache = None

def load_questions() -> Dict:
    """
    Load questions from JSON file
    
    Returns:
        dict: Questions organized by role and skill level
    """
    global _questions_cache
    
    if _questions_cache is not None:
        return _questions_cache
    
    try:
        with open(QUESTIONS_FILE, 'r') as f:
            _questions_cache = json.load(f)
        return _questions_cache
    except Exception as e:
        print(f"Error loading questions: {str(e)}")
        # Return default questions if file not found
        return {
            "Software Engineer": {
                "Beginner": ["What is Object-Oriented Programming?"],
                "Intermediate": ["Explain design patterns."],
                "Advanced": ["Design a scalable system."]
            }
        }

def get_questions_for_role(
    job_role: str,
    skill_level: str = 'Beginner',
    count: int = 5
) -> List[Dict]:
    """
    Get interview questions for specific role and skill level
    
    Args:
        job_role: Job role (e.g., 'Software Engineer')
        skill_level: Skill level ('Beginner', 'Intermediate', 'Advanced')
        count: Number of questions to return
        
    Returns:
        list: List of question dictionaries
    """
    questions_data = load_questions()
    
    # Check if role exists
    if job_role not in questions_data:
        # Default to Software Engineer if role not found
        job_role = 'Software Engineer'
    
    # Check if skill level exists
    if skill_level not in questions_data[job_role]:
        skill_level = 'Beginner'
    
    # Get questions for the specified role and level
    available_questions = questions_data[job_role][skill_level]
    
    # Randomly select questions
    selected_count = min(count, len(available_questions))
    selected_questions = random.sample(available_questions, selected_count)
    
    # Format questions with metadata
    formatted_questions = []
    for idx, question_text in enumerate(selected_questions):
        formatted_questions.append({
            'id': f'q_{idx + 1}',
            'question': question_text,
            'job_role': job_role,
            'skill_level': skill_level,
            'order': idx + 1
        })
    
    return formatted_questions

def generate_follow_up_question(
    original_question: str,
    answer: str,
    job_role: str
) -> Dict:
    """
    Generate a follow-up question based on the answer
    This is a simplified implementation
    
    Args:
        original_question: The original question
        answer: User's answer
        job_role: Job role
        
    Returns:
        dict: Follow-up question
    """
    # Simple follow-up templates
    follow_up_templates = [
        f"Can you elaborate more on that?",
        f"How would you apply this in a real-world scenario?",
        f"What challenges might you face with this approach?",
        f"Can you provide a specific example?",
        f"How does this relate to {job_role} best practices?"
    ]
    
    follow_up = random.choice(follow_up_templates)
    
    return {
        'id': 'follow_up',
        'question': follow_up,
        'job_role': job_role,
        'is_follow_up': True,
        'original_question': original_question
    }

def get_available_roles() -> List[str]:
    """
    Get list of available job roles
    
    Returns:
        list: List of job roles
    """
    questions_data = load_questions()
    return list(questions_data.keys())

def get_available_skill_levels() -> List[str]:
    """
    Get list of available skill levels
    
    Returns:
        list: List of skill levels
    """
    return ['Beginner', 'Intermediate', 'Advanced']
