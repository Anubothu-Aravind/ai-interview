import tempfile
import streamlit as st
from gtts import gTTS
import speech_recognition as sr

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        st.audio(f.name)

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as src:
        audio = r.listen(src, timeout=30)
    return r.recognize_google(audio)
