"""
Fluency Test Model
Represents fluency test data structure in Supabase PostgreSQL
"""

from database.supabase_config import get_supabase_client, FLUENCY_TESTS_TABLE
from datetime import datetime
from typing import Dict, List, Optional

class FluencyTest:
    """Fluency test model for Supabase"""
    
    @staticmethod
    def create(user_id: str, transcript: str, audio_url: Optional[str] = None, 
               fluency_score: float = 0.0, pronunciation_score: float = 0.0,
               grammar_score: float = 0.0, wpm: float = 0.0, 
               pause_count: int = 0, filler_word_count: int = 0,
               feedback: Optional[List] = None, grammar_errors: Optional[List] = None):
        """Create new fluency test"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        # Calculate overall score
        overall_score = round((fluency_score * 0.35 + pronunciation_score * 0.30 + grammar_score * 0.35), 2)
        
        data = {
            'user_id': user_id,
            'transcript': transcript,
            'audio_url': audio_url,
            'fluency_score': int(fluency_score),
            'pronunciation_score': int(pronunciation_score),
            'grammar_score': int(grammar_score),
            'wpm': int(wpm),
            'pause_count': pause_count,
            'filler_word_count': filler_word_count,
            'feedback': feedback or [],
            'grammar_errors': grammar_errors or [],
            'overall_score': int(overall_score)
        }
        
        result = supabase.table(FLUENCY_TESTS_TABLE).insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_by_id(test_id: str):
        """Get fluency test by ID"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(FLUENCY_TESTS_TABLE).select('*').eq('id', test_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_tests(user_id: str, limit: int = 10):
        """Get user's fluency tests"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(FLUENCY_TESTS_TABLE)\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        return result.data
    
    @staticmethod
    def update(test_id: str, data: Dict):
        """Update fluency test"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(FLUENCY_TESTS_TABLE).update(data).eq('id', test_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def delete(test_id: str):
        """Delete fluency test"""
        supabase = get_supabase_client()
        
        if supabase is None:
            raise Exception("Database not available")
        
        result = supabase.table(FLUENCY_TESTS_TABLE).delete().eq('id', test_id).execute()
        return result.data
