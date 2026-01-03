"""
Resume Model
Represents resume data structure in Firestore
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid

class Resume:
    """Resume model with content and analysis results"""
    
    def __init__(
        self,
        user_id: str,
        resume_id: Optional[str] = None,
        content: Optional[Dict] = None,
        analysis: Optional[Dict] = None,
        score: float = 0.0,
        suggestions: Optional[List[str]] = None,
        file_url: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        self.resume_id = resume_id or str(uuid.uuid4())
        self.user_id = user_id
        self.content = content or {}
        self.analysis = analysis or {}
        self.score = score
        self.suggestions = suggestions or []
        self.file_url = file_url
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert resume to dictionary for Firestore"""
        return {
            'resume_id': self.resume_id,
            'user_id': self.user_id,
            'content': self.content,
            'analysis': self.analysis,
            'score': self.score,
            'suggestions': self.suggestions,
            'file_url': self.file_url,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Resume':
        """Create Resume from Firestore document"""
        return Resume(
            resume_id=data.get('resume_id'),
            user_id=data.get('user_id'),
            content=data.get('content', {}),
            analysis=data.get('analysis', {}),
            score=data.get('score', 0.0),
            suggestions=data.get('suggestions', []),
            file_url=data.get('file_url'),
            timestamp=data.get('timestamp')
        )
    
    def set_content(self, content: Dict):
        """Set resume content"""
        self.content = content
    
    def set_analysis(self, analysis: Dict):
        """Set analysis results"""
        self.analysis = analysis
    
    def set_score(self, score: float):
        """Set overall resume score"""
        self.score = score
    
    def add_suggestion(self, suggestion: str):
        """Add an improvement suggestion"""
        self.suggestions.append(suggestion)
    
    def calculate_score(self) -> float:
        """Calculate overall score from analysis components"""
        if not self.analysis:
            return 0.0
        
        # Extract scores from analysis
        grammar_score = self.analysis.get('grammar_score', 0)
        structure_score = self.analysis.get('structure_score', 0)
        ats_score = self.analysis.get('ats_score', 0)
        keyword_score = self.analysis.get('keyword_score', 0)
        
        # Weighted average
        weights = {
            'grammar': 0.25,
            'structure': 0.20,
            'ats': 0.25,
            'keywords': 0.30
        }
        
        self.score = round(
            grammar_score * weights['grammar'] +
            structure_score * weights['structure'] +
            ats_score * weights['ats'] +
            keyword_score * weights['keywords'],
            2
        )
        
        return self.score
    
    def __repr__(self):
        return f"<Resume {self.resume_id} - Score: {self.score}>"
