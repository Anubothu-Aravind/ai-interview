import json
from typing import List, Optional
from openai import OpenAI

from backend.config import settings

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_question(
        self,
        resume: str,
        jd: str,
        interview_type: str,
        question_num: int,
        conversation_history: List[dict]
    ) -> str:
        """Generate interview question based on context"""
        
        # Build conversation context
        context = ""
        if conversation_history:
            context = "\n\nPrevious Questions and Answers:\n"
            for i, qa in enumerate(conversation_history, 1):
                context += f"\nQ{i}: {qa['question']}\nA{i}: {qa['answer']}\n"
        
        prompt = f"""You are conducting a {interview_type} interview.

Job Description:
{jd}

Candidate's Resume:
{resume}

{context}

This is question {question_num} out of 10 questions total.

Generate ONE relevant {interview_type} interview question that:
- Is appropriate for question number {question_num} (start easier, get progressively harder)
- Relates to the job requirements
- Builds upon previous answers if any
- Is specific and clear
- For technical interviews: focus on skills, problem-solving, coding experience
- For HR interviews: focus on soft skills, culture fit, scenarios

Return ONLY the question text, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert technical and HR interviewer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating question: {e}")
            return "Tell me about your relevant experience for this role."
    
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        jd: str,
        interview_type: str
    ) -> tuple[float, str]:
        """Evaluate the candidate's answer"""
        
        prompt = f"""Evaluate this {interview_type} interview answer.

Job Requirements:
{jd}

Question: {question}
Answer: {answer}

Provide:
1. A score from 0-10 (0=poor, 10=excellent)
2. Brief constructive feedback (2-3 sentences)

Consider:
- Relevance to the question
- Depth of knowledge
- Communication clarity
- Alignment with job requirements

Return ONLY valid JSON in this exact format:
{{"score": 8, "feedback": "Your feedback here"}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert interview evaluator. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.5
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean up the response if it has markdown code blocks
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].strip()
            
            result = json.loads(result_text)
            return float(result['score']), result['feedback']
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return 7.0, "Unable to provide detailed feedback at this time."
    
    def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using OpenAI TTS"""
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            return response.content
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            raise
    
    def speech_to_text(self, audio_file) -> str:
        """Convert speech to text using OpenAI Whisper"""
        try:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error in speech-to-text: {e}")
            raise

# Singleton instance
openai_service = OpenAIService()
