# app/database.py
import os
from datetime import datetime
import streamlit as st
from supabase import create_client, Client
from supabase.client import ClientOptions

@st.cache_resource
def init_supabase() -> Client | None:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url or not key:
        st.error("Supabase credentials missing")
        return None

    return create_client(
        url,
        key,
        options=ClientOptions(
            postgrest_client_timeout=30,
            storage_client_timeout=30,
        )
    )

class DatabaseManager:
    def __init__(self, supabase: Client):
        self.supabase = supabase
    def create_tables(self) -> str:
            """
            Returns SQL schema for Supabase (display-only).
            """
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
    def save_interview(self, interview_data):
        response = self.supabase.table("interviews").insert({
            "candidate_name": interview_data["candidate_name"],
            "job_title": interview_data["job_title"],
            "interview_type": interview_data["interview_type"],
            "final_score": interview_data["final_score"],
            "start_time": interview_data["start_time"],
            "completed_at": datetime.now().isoformat(),
        }).execute()

        interview_id = response.data[0]["id"]

        questions = [{
            "interview_id": interview_id,
            "question_number": qa["number"],
            "question_text": qa["question"],
            "answer": qa["answer"],
            "score": qa["score"],
            "feedback": qa["feedback"],
        } for qa in interview_data["qa_pairs"]]

        self.supabase.table("questions").insert(questions).execute()
        return interview_id

    def get_all_interviews(self):
        return self.supabase.table("interviews").select("*").order(
            "created_at", desc=True
        ).execute().data or []

    def get_questions(self, interview_id):
        return self.supabase.table("questions").select("*").eq(
            "interview_id", interview_id
        ).order("question_number").execute().data or []
