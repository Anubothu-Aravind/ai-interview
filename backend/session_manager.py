import uuid
from datetime import datetime
from typing import Dict, List, Optional

from backend.models import InterviewSession, QAPair

class SessionManager:
    """Manage active interview sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, InterviewSession] = {}
        self.conversation_history: Dict[str, List[dict]] = {}
        self.qa_pairs: Dict[str, List[QAPair]] = {}
    
    def create_session(
        self,
        candidate_name: str,
        job_title: str,
        interview_type: str,
        resume: str,
        jd: str
    ) -> str:
        """Create a new interview session"""
        session_id = str(uuid.uuid4())
        
        session = InterviewSession(
            session_id=session_id,
            candidate_name=candidate_name,
            job_title=job_title,
            interview_type=interview_type,
            resume=resume,
            jd=jd,
            start_time=datetime.now(),
            current_question_num=1,
            total_questions=10
        )
        
        self.sessions[session_id] = session
        self.conversation_history[session_id] = []
        self.qa_pairs[session_id] = []
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, **kwargs):
        """Update session attributes"""
        session = self.sessions.get(session_id)
        if session:
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
    
    def add_conversation(self, session_id: str, question: str, answer: str):
        """Add to conversation history"""
        if session_id in self.conversation_history:
            self.conversation_history[session_id].append({
                'question': question,
                'answer': answer
            })
    
    def get_conversation_history(self, session_id: str) -> List[dict]:
        """Get conversation history for session"""
        return self.conversation_history.get(session_id, [])
    
    def add_qa_pair(self, session_id: str, qa_pair: QAPair):
        """Add Q&A pair to session"""
        if session_id in self.qa_pairs:
            self.qa_pairs[session_id].append(qa_pair)
    
    def get_qa_pairs(self, session_id: str) -> List[QAPair]:
        """Get all Q&A pairs for session"""
        return self.qa_pairs.get(session_id, [])
    
    def delete_session(self, session_id: str):
        """Delete session and clean up"""
        self.sessions.pop(session_id, None)
        self.conversation_history.pop(session_id, None)
        self.qa_pairs.pop(session_id, None)

# Singleton instance
session_manager = SessionManager()
