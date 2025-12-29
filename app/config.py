import streamlit as st
from dotenv import load_dotenv

def load_config():
    load_dotenv()

    st.set_page_config(
        page_title="AI Interview System",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(120deg, #1f77b4, #ff7f0e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        .question-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            font-size: 1.3rem;
            margin: 2rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
