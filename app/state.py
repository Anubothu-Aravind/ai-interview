import streamlit as st

def init_session_state():
    defaults = {
        "interview_started": False,
        "current_question_num": 1,
        "current_question": "",
        "interview_data": {},
        "all_qa": [],
        "total_questions": 10,
        "conversation_history": [],
        "interview_id": None,
        "show_history": False,
        "selected_interview_id": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
