"""
Resume Model
Represents resume data structure in Supabase PostgreSQL
"""

from database.supabase_config import get_supabase_client, RESUMES_TABLE
from datetime import datetime
from typing import Dict, List, Optional

class Resume:
    """Resume model for Supabase"""
    
    @staticmethod
    def create(user_id: str, content: Optional[Dict] = None, analysis: Optional[Dict] = None,
               score: float = 0.0, suggestions: Optional[List] = None, file_url: Optional[str] = None,
               resume_type: str = 'uploaded', parsed_text: Optional[str] = None,
               target_job_role: Optional[str] = None):
        """Create new resume"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        data = {
            'user_id': user_id,
            'resume_type': resume_type,
            'file_url': file_url,
            'content': content or {},
            'parsed_text': parsed_text,
            'analysis': analysis or {},
            'overall_score': int(score) if score else None,
            'suggestions': suggestions or [],
            'target_job_role': target_job_role
        }
        
        # Extract individual scores from analysis if available
        if analysis:
            data['ats_score'] = int(analysis.get('ats_score', 0))
            data['grammar_score'] = int(analysis.get('grammar_score', 0))
            data['keyword_match_score'] = int(analysis.get('keyword_score', 0))
        
        result = supabase.table(RESUMES_TABLE).insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_by_id(resume_id: str):
        """Get resume by ID"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(RESUMES_TABLE).select('*').eq('id', resume_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_resumes(user_id: str, limit: int = 10):
        """Get user's resumes"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(RESUMES_TABLE)\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        return result.data
    
    @staticmethod
    def update(resume_id: str, data: Dict):
        """Update resume"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(RESUMES_TABLE).update(data).eq('id', resume_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def delete(resume_id: str):
        """Delete resume"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(RESUMES_TABLE).delete().eq('id', resume_id).execute()
        return result.data
