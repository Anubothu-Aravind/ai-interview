# app/history.py
import streamlit as st
from datetime import datetime


def render_history(db):
    st.markdown("### 📚 Interview History")

    interviews = db.get_all_interviews()

    if not interviews:
        st.info("No interviews found.")
        if st.button("⬅️ Back"):
            st.session_state.show_history = False
            st.rerun()
        return

    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown("#### Past Interviews")

        for interview in interviews:
            label = (
                f"{interview['candidate_name']} | "
                f"{interview['job_title']} | "
                f"{datetime.fromisoformat(interview['created_at']).strftime('%Y-%m-%d')}"
            )

            if st.button(label, key=f"int_{interview['id']}"):
                st.session_state.selected_interview_id = interview["id"]
                st.rerun()

    with col2:
        interview_id = st.session_state.get("selected_interview_id")

        if not interview_id:
            st.info("Select an interview to view details.")
            return

        interview = next(
            (i for i in interviews if i["id"] == interview_id), None
        )

        if not interview:
            st.error("Interview not found.")
            return

        st.markdown("#### Interview Details")
        st.write(f"**Candidate:** {interview['candidate_name']}")
        st.write(f"**Role:** {interview['job_title']}")
        st.write(f"**Type:** {interview['interview_type']}")
        st.write(f"**Final Score:** {interview['final_score']:.1f}/10")
        st.write(
            f"**Date:** "
            f"{datetime.fromisoformat(interview['created_at']).strftime('%B %d, %Y %H:%M')}"
        )

        st.markdown("---")
        st.markdown("#### Questions & Answers")

        questions = db.get_questions(interview_id)

        for q in questions:
            with st.expander(f"Q{q['question_number']} (Score: {q['score']}/10)"):
                st.write("**Question:**", q["question_text"])
                st.write("**Answer:**", q["answer"])
                st.write("**Feedback:**", q["feedback"])

        st.markdown("---")
        if st.button("⬅️ Back to Main"):
            st.session_state.show_history = False
            st.session_state.selected_interview_id = None
            st.rerun()
