# app/audio.py
import tempfile
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import streamlit as st
from scipy.io.wavfile import write
from openai import OpenAI
from pathlib import Path

SAMPLE_RATE = 16000
CHUNK_SECONDS = 1          # waveform refresh
TRANSCRIBE_EVERY = 5       # seconds


def text_to_speech(text: str):
    """Convert text to speech using OpenAI TTS and play it"""
    try:
        client = OpenAI()
        
        # Generate speech audio
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name
        
        # Play the audio using streamlit's audio player
        with open(tmp_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        
        # Clean up temporary file
        Path(tmp_path).unlink(missing_ok=True)
        
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")


def start_recording():
    """Initialize recording session"""
    st.session_state.audio_frames = []
    st.session_state.partial_transcript = ""


def record_chunk():
    """Record a chunk of audio"""
    audio = sd.rec(
        int(CHUNK_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    st.session_state.audio_frames.append(audio)


def draw_waveform():
    """Draw the current audio waveform"""
    if not st.session_state.audio_frames:
        return
    
    audio = np.concatenate(st.session_state.audio_frames, axis=0)
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.plot(audio, linewidth=0.5, color='#1f77b4')
    ax.set_ylim(-1, 1)
    ax.axis("off")
    st.pyplot(fig)
    plt.close(fig)


def transcribe_partial():
    """Transcribe audio recorded so far (for live preview)"""
    if not st.session_state.audio_frames:
        return
    
    tmp_path = None
    try:
        client = OpenAI()
        
        audio = np.concatenate(st.session_state.audio_frames, axis=0)
        
        # Convert float32 audio to int16 for WAV file
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # Create temporary file and close it immediately
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp_path = tmp.name
        tmp.close()
        
        # Write audio to the closed file
        write(tmp_path, SAMPLE_RATE, audio_int16)
        
        # Open and transcribe
        with open(tmp_path, "rb") as f:
            res = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        
        st.session_state.partial_transcript = res.text
        
    except Exception as e:
        st.warning(f"Transcription error: {e}")
    finally:
        # Clean up in finally block
        if tmp_path and Path(tmp_path).exists():
            try:
                Path(tmp_path).unlink()
            except Exception:
                pass  # Ignore cleanup errors


def stop_and_transcribe():
    """Stop recording and return final transcription"""
    if not st.session_state.audio_frames:
        return ""
    
    tmp_path = None
    try:
        client = OpenAI()
        audio = np.concatenate(st.session_state.audio_frames, axis=0)
        
        # Convert float32 audio to int16 for WAV file
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # Create temporary file and close it immediately
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp_path = tmp.name
        tmp.close()
        
        # Write audio to the closed file
        write(tmp_path, SAMPLE_RATE, audio_int16)
        
        # Open and transcribe
        with open(tmp_path, "rb") as f:
            res = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        
        return res.text.strip()
        
    except Exception as e:
        st.error(f"Final transcription error: {e}")
        return ""
    finally:
        # Clean up in finally block to ensure it runs
        if tmp_path and Path(tmp_path).exists():
            try:
                Path(tmp_path).unlink()
            except Exception:
                pass  # Ignore cleanup errors