import os
from datetime import datetime
import streamlit as st
from supabase import create_client, Client
from supabase.client import ClientOptions

@st.cache_resource
def init_supabase() -> Client | None:
    """
    Initialize a configured Supabase client from environment credentials.
    
    Reads SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY from the environment; if either is missing an error is displayed and the function returns None. When credentials are present, returns a Supabase Client configured with 30-second PostgREST and storage timeouts.
    
    Returns:
        Client: Supabase client when credentials are present, `None` otherwise.
    """
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
        """
        Create a DatabaseManager that uses the provided Supabase client for database operations.
        """
        self.supabase = supabase

    def save_interview(self, interview_data):
        """
        Persist an interview record and its associated question-and-answer entries to the database.
        
        Parameters:
            interview_data (dict): Interview payload containing:
                - candidate_name (str)
                - job_title (str)
                - interview_type (str)
                - final_score (numeric)
                - start_time (str|datetime): interview start timestamp
                - qa_pairs (list[dict]): list of QA objects each with keys:
                    - number (int)
                    - question (str)
                    - answer (str)
                    - score (numeric)
                    - feedback (str)
        
        Returns:
            interview_id (int): The ID of the newly inserted interview record.
        """
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
        """
        Retrieve all interview records ordered by creation time descending.
        
        Returns:
            list: A list of interview records (dictionaries). Returns an empty list if no records are found.
        """
        return self.supabase.table("interviews").select("*").order(
            "created_at", desc=True
        ).execute().data or []

    def get_questions(self, interview_id):
        """
        Retrieve all question records for a given interview, ordered by question number.
        
        Parameters:
            interview_id: Identifier of the interview whose questions should be returned.
        
        Returns:
            A list of question record dictionaries ordered by `question_number`; an empty list if no questions are found.
        """
        return self.supabase.table("questions").select("*").eq(
            "interview_id", interview_id
        ).order("question_number").execute().data or []