import tempfile
import streamlit as st
from gtts import gTTS
import speech_recognition as sr

def text_to_speech(text):
    """
    Synthesize English speech from the given text and play the resulting audio in Streamlit.
    
    The text is converted to speech using gTTS, saved to a temporary MP3 file, and played with Streamlit's audio player.
    
    Parameters:
        text (str): Text to synthesize into speech.
    """
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        st.audio(f.name)

def speech_to_text():
    """
    Transcribes speech captured from the default microphone into text.
    
    Records audio from the system default microphone (30 second listen timeout) and returns the recognized text.
    
    Returns:
        transcription (str): The recognized text from the captured audio.
    """
    r = sr.Recognizer()
    with sr.Microphone() as src:
        audio = r.listen(src, timeout=30)
    return r.recognize_google(audio)