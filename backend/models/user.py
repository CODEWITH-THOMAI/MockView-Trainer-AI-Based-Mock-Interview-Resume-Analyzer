"""
User Model
Represents user data structure in Firestore
"""

from datetime import datetime
from typing import Dict, Optional

class User:
    """User model with profile information"""
    
    def __init__(
        self,
        uid: str,
        email: str,
        name: str,
        skill_level: str = 'Beginner',
        job_role: str = 'Software Engineer',
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.uid = uid
        self.email = email
        self.name = name
        self.skill_level = skill_level  # Beginner, Intermediate, Advanced
        self.job_role = job_role
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert user object to dictionary for Firestore"""
        return {
            'uid': self.uid,
            'email': self.email,
            'name': self.name,
            'skill_level': self.skill_level,
            'job_role': self.job_role,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'User':
        """Create User object from Firestore document"""
        return User(
            uid=data.get('uid'),
            email=data.get('email'),
            name=data.get('name'),
            skill_level=data.get('skill_level', 'Beginner'),
            job_role=data.get('job_role', 'Software Engineer'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def update_profile(
        self,
        name: Optional[str] = None,
        skill_level: Optional[str] = None,
        job_role: Optional[str] = None
    ):
        """Update user profile fields"""
        if name:
            self.name = name
        if skill_level:
            self.skill_level = skill_level
        if job_role:
            self.job_role = job_role
        self.updated_at = datetime.now()
    
    def __repr__(self):
        return f"<User {self.email} ({self.job_role} - {self.skill_level})>"
