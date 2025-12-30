# app/state.py
import streamlit as st

def init_session_state():
    defaults = {
        # interview flow
        "interview_started": False,
        "current_question_num": 1,
        "current_question": "",
        "total_questions": 10,
        "conversation_history": [],
        "all_qa": [],

        # question audio
        "question_spoken": False,
        "question_start_time": None,

        # timers (seconds)
        "repeat_window": 120,
        "record_max_time": 300,
        "stop_button_time": 90,
        "preview_time": 20,

        # recording state
        "recording": False,
        "recording_start_time": None,
        "audio_frames": [],
        "partial_transcript": "",

        # modes
        "hr_mode": False,

        # ui
        "show_history": False,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
