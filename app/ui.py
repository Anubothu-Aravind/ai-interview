import streamlit as st
import json
import time
from datetime import datetime

from app.utils import extract_text_from_pdf
from app.audio import text_to_speech, speech_to_text
from app.openai_client import ask_ai_question, evaluate_answer
from app.history import render_history



# ---------- Sidebar ----------
def render_sidebar(supabase_connected: bool, openai_connected: bool, db):
    """
    Render the Streamlit sidebar showing system status, brief usage steps, and utility actions.
    
    Displays Supabase and OpenAI connection status, a "How It Works" walkthrough, a button that sets st.session_state.show_history = True to reveal past interviews, and a button that renders the database SQL schema by calling db.create_tables().
    
    Parameters:
        supabase_connected (bool): True if Supabase is connected.
        openai_connected (bool): True if OpenAI is configured and reachable.
        db: Database interface providing a create_tables() method used to display the SQL schema.
    """
    with st.sidebar:
        st.markdown("### 📊 System Status")
        st.markdown(f"**Supabase:** {'✅ Connected' if supabase_connected else '❌ Not Connected'}")
        st.markdown(f"**OpenAI:** {'✅ Ready' if openai_connected else '❌ Not Configured'}")

        st.markdown("---")
        st.markdown("### 📖 How It Works")
        st.markdown("""
        1. Upload resume & job description  
        2. AI asks 10 questions  
        3. Answer via text or voice  
        4. Get instant feedback  
        5. View final results
        """)

        st.markdown("---")
        if st.button("📚 View Past Interviews"):
            st.session_state.show_history = True

        st.markdown("---")
        if st.button("📋 Show SQL Script"):
            st.code(db.create_tables(), language="sql")


# ---------- Setup Screen ----------
def render_setup(openai_client):
    """
    Render the interview setup screen, collect candidate and job information, and initialize a new interview session when the user starts the interview.
    
    Displays inputs for candidate name, job title, interview type, and file uploaders for a resume and job description (PDF or TXT). If the Start Interview button is pressed and all fields are provided, extracts text from uploaded files, stores interview metadata in session state (including resume and job description text and start time), requests the first AI-generated question, sets session flags to begin the interview, and triggers an app rerun. If required fields are missing, displays a warning and does not start the interview.
    """
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
        st.rerun()


# ---------- Interview Screen ----------
def render_interview(openai_client):
    """
    Render the active interview question UI and handle answer input, recording, evaluation, and progression.
    
    Displays the current question with progress, lets the user hear the question, enter text or record voice for an answer, and submit that answer for AI evaluation. On submit, the function appends the question/answer/score/feedback to session state, updates the conversation history, advances the question counter, fetches the next AI-generated question when more remain, and triggers a rerun to update the app. If the answer is empty, a warning is shown and submission is aborted.
    """
    q_num = st.session_state.current_question_num
    total = st.session_state.total_questions

    st.progress((q_num - 1) / total, text=f"Question {q_num} of {total}")

    st.markdown(f"""
    <div class="question-box">
        <h3>Question {q_num}</h3>
        <p>{st.session_state.current_question}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔊 Hear Question"):
        text_to_speech(st.session_state.current_question)

    answer = st.text_area(
        "Your Answer",
        height=200,
        key=f"answer_{q_num}"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎤 Record Voice"):
            voice = speech_to_text()
            if voice:
                st.session_state[f"answer_{q_num}"] = voice
                st.rerun()

    with col2:
        if st.button("➡️ Submit Answer", type="primary"):
            if not answer.strip():
                st.warning("Answer cannot be empty")
                return

            with st.spinner("🤖 Evaluating answer..."):
                score, feedback = evaluate_answer(
                    openai_client,
                    st.session_state.current_question,
                    answer,
                    st.session_state.interview_data["jd"],
                    st.session_state.interview_data["interview_type"],
                )

            qa = {
                "number": q_num,
                "question": st.session_state.current_question,
                "answer": answer,
                "score": score,
                "feedback": feedback,
            }

            st.session_state.all_qa.append(qa)
            st.session_state.conversation_history.append({
                "question": qa["question"],
                "answer": qa["answer"],
            })

            if q_num < total:
                st.session_state.current_question_num += 1
                st.session_state.current_question = ask_ai_question(
                    openai_client,
                    st.session_state.interview_data["resume"],
                    st.session_state.interview_data["jd"],
                    st.session_state.interview_data["interview_type"],
                    st.session_state.current_question_num,
                    st.session_state.conversation_history,
                )
                time.sleep(1)
                st.rerun()
            else:
                st.session_state.current_question_num += 1
                st.rerun()


# ---------- Results Screen ----------
def render_results(db):
    """
    Render the interview results screen, show per-question feedback, and provide options to save or download the interview data.
    
    Displays the overall numeric and percentage score computed from `st.session_state.all_qa`, creates expandable sections for each question/answer/feedback pair, and renders controls to save the interview to the provided database and to download the QA pairs as a JSON file.
    
    Parameters:
        db: A persistence interface with a `save_interview` method used to store the interview record when the user chooses to save it.
    """
    scores = [qa["score"] for qa in st.session_state.all_qa]
    avg = sum(scores) / len(scores)
    pct = (avg / 10) * 100

    st.markdown("### 🎉 Interview Completed")
    st.metric("Overall Score", f"{avg:.1f}/10", f"{pct:.0f}%")

    for qa in st.session_state.all_qa:
        with st.expander(f"Q{qa['number']} (Score: {qa['score']}/10)"):
            st.write("**Question:**", qa["question"])
            st.write("**Answer:**", qa["answer"])
            st.write("**Feedback:**", qa["feedback"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save to Database"):
            data = st.session_state.interview_data | {
                "qa_pairs": st.session_state.all_qa,
                "final_score": avg,
            }
            db.save_interview(data)
            st.success("Interview saved")

    with col2:
        st.download_button(
            "📥 Download JSON",
            json.dumps(st.session_state.all_qa, indent=2),
            file_name="interview_results.json",
        )


# ---------- App Orchestrator ----------
def render_app(db, openai_client):
    """
    Render the main Streamlit UI and route to the appropriate app view.
    
    Displays the header and sidebar, then selects and renders one of: past-interviews history, setup screen, active interview flow, or final results based on Streamlit session state.
    """
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