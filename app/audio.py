# app/audio.py
import tempfile
import streamlit as st
from gtts import gTTS
import speech_recognition as sr


def text_to_speech(text: str):
    if not text:
        return

    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        st.audio(f.name)


def speech_to_text() -> str:
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎙️ Listening... Speak clearly")
            r.adjust_for_ambient_noise(source, duration=0.6)
            audio = r.listen(source, timeout=5, phrase_time_limit=15)

        return r.recognize_google(audio)

    except sr.WaitTimeoutError:
        st.warning("⏱️ Listening timed out. Try again.")
        return ""

    except sr.UnknownValueError:
        st.warning("⚠️ Could not understand audio. Please try again.")
        return ""

    except sr.RequestError as e:
        st.error(f"❌ Speech service error: {e}")
        return ""

    except Exception as e:
        st.error(f"❌ Microphone error: {e}")
        return ""
