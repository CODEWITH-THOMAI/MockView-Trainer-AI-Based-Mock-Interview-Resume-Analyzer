"""
Fluency Test Model
Represents fluency test data structure in Firestore
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid

class FluencyTest:
    """Fluency test model with transcript and analysis results"""
    
    def __init__(
        self,
        user_id: str,
        test_id: Optional[str] = None,
        transcript: str = '',
        audio_duration: float = 0.0,
        fluency_score: float = 0.0,
        pronunciation_score: float = 0.0,
        grammar_score: float = 0.0,
        wpm: float = 0.0,
        pause_count: int = 0,
        filler_word_count: int = 0,
        feedback: Optional[List[str]] = None,
        detailed_analysis: Optional[Dict] = None,
        timestamp: Optional[datetime] = None
    ):
        self.test_id = test_id or str(uuid.uuid4())
        self.user_id = user_id
        self.transcript = transcript
        self.audio_duration = audio_duration
        self.fluency_score = fluency_score
        self.pronunciation_score = pronunciation_score
        self.grammar_score = grammar_score
        self.wpm = wpm
        self.pause_count = pause_count
        self.filler_word_count = filler_word_count
        self.feedback = feedback or []
        self.detailed_analysis = detailed_analysis or {}
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert fluency test to dictionary for Firestore"""
        return {
            'test_id': self.test_id,
            'user_id': self.user_id,
            'transcript': self.transcript,
            'audio_duration': self.audio_duration,
            'fluency_score': self.fluency_score,
            'pronunciation_score': self.pronunciation_score,
            'grammar_score': self.grammar_score,
            'wpm': self.wpm,
            'pause_count': self.pause_count,
            'filler_word_count': self.filler_word_count,
            'feedback': self.feedback,
            'detailed_analysis': self.detailed_analysis,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'FluencyTest':
        """Create FluencyTest from Firestore document"""
        return FluencyTest(
            test_id=data.get('test_id'),
            user_id=data.get('user_id'),
            transcript=data.get('transcript', ''),
            audio_duration=data.get('audio_duration', 0.0),
            fluency_score=data.get('fluency_score', 0.0),
            pronunciation_score=data.get('pronunciation_score', 0.0),
            grammar_score=data.get('grammar_score', 0.0),
            wpm=data.get('wpm', 0.0),
            pause_count=data.get('pause_count', 0),
            filler_word_count=data.get('filler_word_count', 0),
            feedback=data.get('feedback', []),
            detailed_analysis=data.get('detailed_analysis', {}),
            timestamp=data.get('timestamp')
        )
    
    def calculate_overall_score(self) -> float:
        """Calculate overall fluency score from components"""
        # Weighted average of scores
        weights = {
            'fluency': 0.35,
            'pronunciation': 0.30,
            'grammar': 0.35
        }
        
        overall = (
            self.fluency_score * weights['fluency'] +
            self.pronunciation_score * weights['pronunciation'] +
            self.grammar_score * weights['grammar']
        )
        
        return round(overall, 2)
    
    def __repr__(self):
        return f"<FluencyTest {self.test_id} - Score: {self.calculate_overall_score()}>"
