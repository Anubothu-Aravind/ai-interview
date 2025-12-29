import os
import json
import streamlit as st
from openai import OpenAI

@st.cache_resource
def init_openai():
    """
    Initialize and return an OpenAI client using the OPENAI_API_KEY environment variable.
    
    If the environment variable is not set, displays an error via Streamlit and returns `None`.
    
    Returns:
        OpenAI or None: An OpenAI client configured with the `OPENAI_API_KEY`, or `None` if the key is missing.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        st.error("OpenAI API key missing")
        return None
    return OpenAI(api_key=key)

def ask_ai_question(client, resume, jd, interview_type, q_num, history):
    """
    Generate the next interview question based on the provided job description, candidate resume, and prior Q/A history.
    
    Parameters:
        resume (str): Candidate resume text to inform question content.
        jd (str): Job description to align the question with role requirements.
        interview_type (str): Type of interview (e.g., "behavioral", "technical") to shape question style.
        q_num (int): Sequence number of the question to generate (e.g., 3 for "question 3/10").
        history (list[dict]): List of previous Q/A pairs; each item should have keys 'question' and 'answer'.
    
    Returns:
        str: The generated interview question text.
    """
    context = ""
    for i, qa in enumerate(history, 1):
        context += f"\nQ{i}: {qa['question']}\nA{i}: {qa['answer']}\n"

    prompt = f"""
Job Description:
{jd}

Resume:
{resume}

{context}

Generate question {q_num}/10 for a {interview_type} interview.
"""

    res = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return res.choices[0].message.content.strip()

def evaluate_answer(client, question, answer, jd, interview_type):
    """
    Evaluate a candidate's answer to a question in the context of a job description and return the model's JSON evaluation.
    
    Parameters:
        question (str): The interview question that was asked.
        answer (str): The candidate's answer to evaluate.
        jd (str): The job description providing context for evaluation.
        interview_type (str): The interview stage or role-specific type to guide evaluation.
    
    Returns:
        dict: The parsed JSON object returned by the model containing evaluation details (e.g., scores, feedback, and any suggested improvements).
    """
    prompt = f"""
Evaluate this answer and return JSON only.

Question: {question}
Answer: {answer}
"""

    res = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return json.loads(res.choices[0].message.content)