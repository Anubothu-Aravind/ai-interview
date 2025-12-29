import streamlit as st

def init_session_state():
    """
    Initialize Streamlit session state with a set of default keys used by the interview flow.
    
    Sets the following keys only if they are not already present in st.session_state:
    - "interview_started": False
    - "current_question_num": 1
    - "current_question": ""
    - "interview_data": {}
    - "all_qa": []
    - "total_questions": 10
    - "conversation_history": []
    - "interview_id": None
    - "show_history": False
    - "selected_interview_id": None
    
    Existing session state values are preserved; only missing keys are added.
    """
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