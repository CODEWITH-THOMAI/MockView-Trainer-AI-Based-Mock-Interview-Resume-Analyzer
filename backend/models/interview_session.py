"""
Interview Session Model
Represents interview session data structure in Firestore
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid

class InterviewSession:
    """Interview session model with questions, answers, and evaluation"""
    
    def __init__(
        self,
        user_id: str,
        job_role: str,
        skill_level: str = 'Beginner',
        session_id: Optional[str] = None,
        questions: Optional[List[Dict]] = None,
        answers: Optional[List[Dict]] = None,
        scores: Optional[Dict] = None,
        feedback: Optional[Dict] = None,
        overall_score: float = 0.0,
        timestamp: Optional[datetime] = None
    ):
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.job_role = job_role
        self.skill_level = skill_level
        self.questions = questions or []
        self.answers = answers or []
        self.scores = scores or {}
        self.feedback = feedback or {}
        self.overall_score = overall_score
        self.timestamp = timestamp or datetime.now()
        self.status = 'in_progress'  # in_progress, completed
    
    def to_dict(self) -> Dict:
        """Convert interview session to dictionary for Firestore"""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'job_role': self.job_role,
            'skill_level': self.skill_level,
            'questions': self.questions,
            'answers': self.answers,
            'scores': self.scores,
            'feedback': self.feedback,
            'overall_score': self.overall_score,
            'timestamp': self.timestamp,
            'status': self.status
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'InterviewSession':
        """Create InterviewSession from Firestore document"""
        session = InterviewSession(
            session_id=data.get('session_id'),
            user_id=data.get('user_id'),
            job_role=data.get('job_role'),
            skill_level=data.get('skill_level', 'Beginner'),
            questions=data.get('questions', []),
            answers=data.get('answers', []),
            scores=data.get('scores', {}),
            feedback=data.get('feedback', {}),
            overall_score=data.get('overall_score', 0.0),
            timestamp=data.get('timestamp')
        )
        session.status = data.get('status', 'in_progress')
        return session
    
    def add_question(self, question: Dict):
        """Add a question to the session"""
        self.questions.append(question)
    
    def add_answer(self, answer: Dict):
        """Add an answer to the session"""
        self.answers.append(answer)
    
    def set_scores(self, scores: Dict):
        """Set evaluation scores"""
        self.scores = scores
    
    def set_feedback(self, feedback: Dict):
        """Set feedback for the session"""
        self.feedback = feedback
    
    def calculate_overall_score(self):
        """Calculate overall score from individual scores"""
        if not self.scores:
            return 0.0
        
        # Calculate average of all scores
        score_values = [s.get('score', 0) for s in self.scores.values() if isinstance(s, dict)]
        if score_values:
            self.overall_score = sum(score_values) / len(score_values)
        return self.overall_score
    
    def complete(self):
        """Mark session as completed"""
        self.status = 'completed'
        self.calculate_overall_score()
    
    def __repr__(self):
        return f"<InterviewSession {self.session_id} - {self.job_role} ({self.status})>"
