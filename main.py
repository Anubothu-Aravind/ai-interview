import streamlit as st
from app.config import load_config
from app.state import init_session_state
from app.database import init_supabase, DatabaseManager
from app.openai_client import init_openai
from app.ui import render_app

def main():
    load_config()
    init_session_state()

    supabase = init_supabase()
    openai_client = init_openai()
    db = DatabaseManager(supabase)

    render_app(db, openai_client)

if __name__ == "__main__":
    main()
