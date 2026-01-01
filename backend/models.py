from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Interview Setup Models
class InterviewSetup(BaseModel):
    candidate_name: str
    job_title: str
    interview_type: str  # "technical" or "hr"
    resume_text: str
    jd_text: str

class InterviewSession(BaseModel):
    session_id: str
    candidate_name: str
    job_title: str
    interview_type: str
    resume: str
    jd: str
    start_time: datetime
    current_question_num: int = 1
    total_questions: int = 10

# Question Models
class Question(BaseModel):
    question_number: int
    question_text: str

class QuestionRequest(BaseModel):
    session_id: str
    question_number: int

# Answer Models
class AnswerSubmission(BaseModel):
    session_id: str
    question_number: int
    question_text: str
    answer_text: str

class AnswerEvaluation(BaseModel):
    score: float
    feedback: str

# Q&A Pair
class QAPair(BaseModel):
    number: int
    question: str
    answer: str
    score: float
    feedback: str

# Interview Results
class InterviewResults(BaseModel):
    session_id: str
    candidate_name: str
    job_title: str
    interview_type: str
    final_score: float
    percentage: float
    qa_pairs: List[QAPair]
    start_time: datetime
    completed_at: datetime

# Database Models
class InterviewDB(BaseModel):
    id: Optional[str] = None
    candidate_name: str
    job_title: str
    interview_type: str
    final_score: float
    start_time: str
    completed_at: str
    created_at: Optional[str] = None

class QuestionDB(BaseModel):
    id: Optional[str] = None
    interview_id: str
    question_number: int
    question_text: str
    answer: str
    score: float
    feedback: str
    created_at: Optional[str] = None

# Audio Models
class TTSRequest(BaseModel):
    text: str

class STTRequest(BaseModel):
    audio_data: str  # base64 encoded audio

class AudioResponse(BaseModel):
    success: bool
    data: Optional[str] = None
    error: Optional[str] = None

# File Upload Models
class FileUploadResponse(BaseModel):
    success: bool
    text: str
    error: Optional[str] = None
