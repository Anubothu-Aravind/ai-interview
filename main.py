import streamlit as st
from app.config import load_config
from app.state import init_session_state
from app.database import init_supabase, DatabaseManager
from app.openai_client import init_openai
from app.ui import render_app

def main():
    """
    Application entry point that initializes configuration and external services, then launches the user interface.
    
    Initializes application configuration and Streamlit session state, creates Supabase and OpenAI clients, constructs a DatabaseManager using the Supabase client, and hands control to the UI renderer with the database manager and OpenAI client.
    """
    load_config()
    init_session_state()

    supabase = init_supabase()
    openai_client = init_openai()
    db = DatabaseManager(supabase)

    render_app(db, openai_client)

if __name__ == "__main__":
    main()