"""
User Model
Represents user data structure in Supabase PostgreSQL
"""

from database.supabase_config import get_supabase_client, USERS_TABLE
from datetime import datetime
from typing import Dict, Optional

class User:
    """User model for Supabase PostgreSQL"""
    
    @staticmethod
    def create(email: str, name: str, skill_level: str = 'Beginner', job_role: str = 'Software Engineer', user_id: Optional[str] = None):
        """Create new user in database"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        data = {
            'email': email,
            'name': name,
            'skill_level': skill_level,
            'job_role': job_role
        }
        
        if user_id:
            data['id'] = user_id
        
        result = supabase.table(USERS_TABLE).insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_by_id(user_id: str):
        """Get user by ID"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(USERS_TABLE).select('*').eq('id', user_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_by_email(email: str):
        """Get user by email"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(USERS_TABLE).select('*').eq('email', email).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def update(user_id: str, data: Dict):
        """Update user profile"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(USERS_TABLE).update(data).eq('id', user_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def delete(user_id: str):
        """Delete user"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(USERS_TABLE).delete().eq('id', user_id).execute()
        return result.data
