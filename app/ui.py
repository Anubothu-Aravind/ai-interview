# app/ui.py
import streamlit as st
import json
import time
from datetime import datetime

from app.utils import extract_text_from_pdf
from app.audio import (
    text_to_speech,
    start_recording,
    record_chunk,
    draw_waveform,
    transcribe_partial,
    stop_and_transcribe,
)
from app.openai_client import ask_ai_question, evaluate_answer
from app.history import render_history


# ---------- Sidebar ----------
def render_sidebar(supabase_connected: bool, openai_connected: bool, db):
    with st.sidebar:
        st.markdown("### 📊 System Status")
        st.markdown(f"**Supabase:** {'✅ Connected' if supabase_connected else '❌ Not Connected'}")
        st.markdown(f"**OpenAI:** {'✅ Ready' if openai_connected else '❌ Not Configured'}")

        st.markdown("---")
        if st.button("📚 View Past Interviews"):
            st.session_state.show_history = True

        st.markdown("---")
        if st.button("📋 Show SQL Script"):
            st.code(db.create_tables(), language="sql")


# ---------- Setup Screen ----------
def render_setup(openai_client):
    st.markdown("### 📋 Interview Setup")

    col1, col2 = st.columns(2)

    with col1:
        candidate_name = st.text_input("👤 Candidate Name")
        job_title = st.text_input("💼 Job Title")
        interview_type = st.selectbox("📝 Interview Type", ["technical", "hr"])

    with col2:
        resume_file = st.file_uploader("Resume (PDF or TXT)", ["pdf", "txt"])
        jd_file = st.file_uploader("Job Description (PDF or TXT)", ["pdf", "txt"])

    if st.button("🚀 Start Interview", type="primary", use_container_width=True):
        if not all([candidate_name, job_title, resume_file, jd_file]):
            st.warning("⚠️ Please complete all fields")
            return

        resume_text = (
            extract_text_from_pdf(resume_file)
            if resume_file.type == "application/pdf"
            else resume_file.read().decode("utf-8")
        )

        jd_text = (
            extract_text_from_pdf(jd_file)
            if jd_file.type == "application/pdf"
            else jd_file.read().decode("utf-8")
        )

        st.session_state.interview_data = {
            "candidate_name": candidate_name,
            "job_title": job_title,
            "interview_type": interview_type,
            "resume": resume_text,
            "jd": jd_text,
            "start_time": datetime.now().isoformat(),
        }

        st.session_state.hr_mode = interview_type == "hr"

        with st.spinner("🤖 Preparing first question..."):
            st.session_state.current_question = ask_ai_question(
                openai_client,
                resume_text,
                jd_text,
                interview_type,
                1,
                [],
            )

        st.session_state.interview_started = True
        st.session_state.current_question_num = 1
        st.session_state.question_spoken = False
        st.session_state.recording = False
        st.rerun()


# ---------- Interview Screen ----------
def render_interview(openai_client):
    q_num = st.session_state.current_question_num
    now = time.time()

    st.progress((q_num - 1) / st.session_state.total_questions)

    st.markdown(
        f"""
        <div class="question-box">
            <h3>Question {q_num}</h3>
            <p>{st.session_state.current_question}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 🔊 Auto-speak question once
    if not st.session_state.question_spoken:
        text_to_speech(st.session_state.current_question)
        st.session_state.question_spoken = True
        st.session_state.question_start_time = now

    elapsed = now - st.session_state.question_start_time

    # 🔁 Repeat allowed for 2 minutes
    if elapsed <= st.session_state.repeat_window:
        if st.button("🔁 Repeat Question"):
            text_to_speech(st.session_state.current_question)
    else:
        st.caption("🔒 Repeat disabled")

    # ⏱️ Start recording after repeat window
    if elapsed > st.session_state.repeat_window and not st.session_state.recording:
        for i in [3, 2, 1]:
            st.warning(f"Recording starts in {i}...")
            time.sleep(1)

        st.session_state.recording = True
        st.session_state.recording_start_time = time.time()
        start_recording()
        st.rerun()

    # 🎙️ Recording phase
    if st.session_state.recording:
        rec_elapsed = time.time() - st.session_state.recording_start_time
        remaining = st.session_state.record_max_time - rec_elapsed

        st.info(f"🎙️ Recording… {int(remaining)} seconds remaining")

        record_chunk()
        draw_waveform()

        # Partial transcription every 5s
        if int(rec_elapsed) % 5 == 0:
            transcribe_partial()

        # Show live transcript near end
        if remaining <= st.session_state.preview_time:
            st.text_area(
                "Live Transcription Preview",
                value=st.session_state.partial_transcript,
                height=150,
            )

        # Stop button after 1.5 min
        if rec_elapsed >= st.session_state.stop_button_time:
            if st.button("⏹️ Stop & Submit"):
                finalize_answer(openai_client)
                return

        # Auto stop
        if remaining <= 0:
            finalize_answer(openai_client)
            return

        time.sleep(0.1)
        st.rerun()


# ---------- Finalize Answer ----------
def finalize_answer(openai_client):
    answer = stop_and_transcribe()
    q = st.session_state.current_question

    score, feedback = evaluate_answer(
        openai_client,
        q,
        answer,
        st.session_state.interview_data["jd"],
        st.session_state.interview_data["interview_type"],
    )

    st.session_state.all_qa.append({
        "number": st.session_state.current_question_num,
        "question": q,
        "answer": answer,
        "score": score,
        "feedback": feedback,
    })

    st.session_state.conversation_history.append({
        "question": q,
        "answer": answer,
    })

    # Reset states
    st.session_state.question_spoken = False
    st.session_state.recording = False
    st.session_state.partial_transcript = ""

    st.session_state.current_question_num += 1

    if st.session_state.current_question_num <= st.session_state.total_questions:
        st.session_state.current_question = ask_ai_question(
            openai_client,
            st.session_state.interview_data["resume"],
            st.session_state.interview_data["jd"],
            st.session_state.interview_data["interview_type"],
            st.session_state.current_question_num,
            st.session_state.conversation_history,
        )

    st.rerun()


# ---------- Results ----------
def render_results(db):
    scores = [qa["score"] for qa in st.session_state.all_qa]
    avg = sum(scores) / len(scores)

    st.markdown("### 🎉 Interview Completed")
    st.metric("Overall Score", f"{avg:.1f}/10")

    for qa in st.session_state.all_qa:
        with st.expander(f"Q{qa['number']}"):
            st.write("**Question:**", qa["question"])
            st.write("**Answer:**", qa["answer"])
            st.write("**Feedback:**", qa["feedback"])

    if st.button("💾 Save Interview"):
        db.save_interview(
            st.session_state.interview_data | {
                "qa_pairs": st.session_state.all_qa,
                "final_score": avg,
            }
        )
        st.success("Saved successfully")


# ---------- App Orchestrator ----------
def render_app(db, openai_client):
    st.markdown('<div class="main-header">🎯 AI Interview System</div>', unsafe_allow_html=True)

    render_sidebar(bool(db.supabase), bool(openai_client), db)

    if st.session_state.show_history:
        render_history(db)
    elif not st.session_state.interview_started:
        render_setup(openai_client)
    elif st.session_state.current_question_num <= st.session_state.total_questions:
        render_interview(openai_client)
    else:
        render_results(db)
