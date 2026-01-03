"""
Interview Session Model
Represents interview session data structure in Supabase PostgreSQL
"""

from database.supabase_config import get_supabase_client, INTERVIEW_SESSIONS_TABLE
from datetime import datetime
from typing import Dict, List, Optional

class InterviewSession:
    """Interview session model for Supabase"""
    
    @staticmethod
    def create(user_id: str, job_role: str, skill_level: str, questions: List[Dict], interview_type: str = 'text'):
        """Create new interview session"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        data = {
            'user_id': user_id,
            'job_role': job_role,
            'skill_level': skill_level,
            'interview_type': interview_type,
            'questions': questions,
            'answers': [],
            'status': 'in_progress'
        }
        
        result = supabase.table(INTERVIEW_SESSIONS_TABLE).insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_by_id(session_id: str):
        """Get session by ID"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(INTERVIEW_SESSIONS_TABLE).select('*').eq('id', session_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def update(session_id: str, data: Dict):
        """Update interview session"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(INTERVIEW_SESSIONS_TABLE).update(data).eq('id', session_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_sessions(user_id: str, limit: int = 10):
        """Get user's interview sessions"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(INTERVIEW_SESSIONS_TABLE)\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        return result.data
    
    @staticmethod
    def delete(session_id: str):
        """Delete session"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(INTERVIEW_SESSIONS_TABLE).delete().eq('id', session_id).execute()
        return result.data
