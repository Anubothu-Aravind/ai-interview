import os
import json
import streamlit as st
from openai import OpenAI

@st.cache_resource
def init_openai():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        st.error("OpenAI API key missing")
        return None
    return OpenAI(api_key=key)

def ask_ai_question(client, resume, jd, interview_type, q_num, history):
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
