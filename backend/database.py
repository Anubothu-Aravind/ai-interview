import os
from datetime import datetime
from typing import List, Optional
from supabase import create_client, Client
from supabase.client import ClientOptions

from backend.config import settings
from backend.models import InterviewDB, QuestionDB, QAPair

class DatabaseService:
    def __init__(self):
        self.client: Optional[Client] = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Supabase client"""
        try:
            self.client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_ROLE_KEY,
                options=ClientOptions(
                    postgrest_client_timeout=30,
                    storage_client_timeout=30,
                )
            )
        except Exception as e:
            print(f"Failed to initialize Supabase: {e}")
            self.client = None
    
    def save_interview(self, interview_data: dict) -> Optional[str]:
        """Save interview to database"""
        if not self.client:
            return None
        
        try:
            # Insert interview
            response = self.client.table('interviews').insert({
                'candidate_name': interview_data['candidate_name'],
                'job_title': interview_data['job_title'],
                'interview_type': interview_data['interview_type'],
                'final_score': interview_data['final_score'],
                'start_time': interview_data['start_time'],
                'completed_at': datetime.now().isoformat(),
            }).execute()
            
            if not response.data:
                return None
            
            interview_id = response.data[0]['id']
            
            # Insert questions
            questions_data = []
            for qa in interview_data['qa_pairs']:
                questions_data.append({
                    'interview_id': interview_id,
                    'question_number': qa['number'],
                    'question_text': qa['question'],
                    'answer': qa['answer'],
                    'score': qa['score'],
                    'feedback': qa['feedback']
                })
            
            self.client.table('questions').insert(questions_data).execute()
            
            return interview_id
        except Exception as e:
            print(f"Error saving interview: {e}")
            return None
    
    def get_all_interviews(self) -> List[dict]:
        """Get all interviews"""
        if not self.client:
            return []
        
        try:
            response = self.client.table('interviews').select('*').order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching interviews: {e}")
            return []
    
    def get_interview_by_id(self, interview_id: str) -> Optional[dict]:
        """Get interview by ID"""
        if not self.client:
            return None
        
        try:
            response = self.client.table('interviews').select('*').eq('id', interview_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching interview: {e}")
            return None
    
    def get_questions(self, interview_id: str) -> List[dict]:
        """Get questions for an interview"""
        if not self.client:
            return []
        
        try:
            response = self.client.table('questions').select('*').eq('interview_id', interview_id).order('question_number').execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching questions: {e}")
            return []
    
    @staticmethod
    def get_table_schema() -> str:
        """Return SQL schema for creating tables"""
        return """
        -- Interview sessions
        CREATE TABLE IF NOT EXISTS interviews (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            candidate_name TEXT NOT NULL,
            job_title TEXT NOT NULL,
            interview_type TEXT NOT NULL,
            final_score FLOAT,
            start_time TIMESTAMP,
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT NOW()
        );

        -- Questions and answers
        CREATE TABLE IF NOT EXISTS questions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            interview_id UUID REFERENCES interviews(id) ON DELETE CASCADE,
            question_number INT,
            question_text TEXT,
            answer TEXT,
            score FLOAT,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """

# Singleton instance
db_service = DatabaseService()
