from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from datetime import datetime
from typing import List
import io
import base64

from backend.config import settings
from backend.models import (
    InterviewSetup,
    Question,
    QuestionRequest,
    AnswerSubmission,
    AnswerEvaluation,
    InterviewResults,
    QAPair,
    TTSRequest,
    AudioResponse,
    FileUploadResponse
)
from backend.database import db_service
from backend.openai_service import openai_service
from backend.session_manager import session_manager
from backend.utils import extract_text_from_pdf, extract_text_from_txt, validate_file_extension

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "supabase_connected": db_service.client is not None,
        "openai_configured": True
    }

# File upload endpoints
@app.post(f"{settings.API_PREFIX}/upload/pdf", response_model=FileUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and extract text from PDF"""
    if not validate_file_extension(file.filename, ['.pdf']):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    try:
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        text = extract_text_from_pdf(content)
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        return FileUploadResponse(success=True, text=text)
    except Exception as e:
        return FileUploadResponse(success=False, text="", error=str(e))

@app.post(f"{settings.API_PREFIX}/upload/txt", response_model=FileUploadResponse)
async def upload_txt(file: UploadFile = File(...)):
    """Upload and read text from TXT"""
    if not validate_file_extension(file.filename, ['.txt']):
        raise HTTPException(status_code=400, detail="Only TXT files allowed")
    
    try:
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        text = extract_text_from_txt(content)
        if not text:
            raise HTTPException(status_code=400, detail="Could not read text file")
        
        return FileUploadResponse(success=True, text=text)
    except Exception as e:
        return FileUploadResponse(success=False, text="", error=str(e))

# Interview session endpoints
@app.post(f"{settings.API_PREFIX}/interview/start")
async def start_interview(setup: InterviewSetup):
    """Start a new interview session"""
    try:
        # Create session
        session_id = session_manager.create_session(
            candidate_name=setup.candidate_name,
            job_title=setup.job_title,
            interview_type=setup.interview_type,
            resume=setup.resume_text,
            jd=setup.jd_text
        )
        
        # Generate first question
        first_question = openai_service.generate_question(
            resume=setup.resume_text,
            jd=setup.jd_text,
            interview_type=setup.interview_type,
            question_num=1,
            conversation_history=[]
        )
        
        return {
            "session_id": session_id,
            "first_question": first_question,
            "total_questions": 10
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(f"{settings.API_PREFIX}/interview/question", response_model=Question)
async def get_next_question(request: QuestionRequest):
    """Get next question for interview"""
    try:
        session = session_manager.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        conversation_history = session_manager.get_conversation_history(request.session_id)
        
        question_text = openai_service.generate_question(
            resume=session.resume,
            jd=session.jd,
            interview_type=session.interview_type,
            question_num=request.question_number,
            conversation_history=conversation_history
        )
        
        return Question(
            question_number=request.question_number,
            question_text=question_text
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(f"{settings.API_PREFIX}/interview/answer", response_model=AnswerEvaluation)
async def submit_answer(submission: AnswerSubmission):
    """Submit and evaluate answer"""
    try:
        session = session_manager.get_session(submission.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Evaluate answer
        score, feedback = openai_service.evaluate_answer(
            question=submission.question_text,
            answer=submission.answer_text,
            jd=session.jd,
            interview_type=session.interview_type
        )
        
        # Store Q&A pair
        qa_pair = QAPair(
            number=submission.question_number,
            question=submission.question_text,
            answer=submission.answer_text,
            score=score,
            feedback=feedback
        )
        session_manager.add_qa_pair(submission.session_id, qa_pair)
        
        # Add to conversation history
        session_manager.add_conversation(
            submission.session_id,
            submission.question_text,
            submission.answer_text
        )
        
        # Update session
        session_manager.update_session(
            submission.session_id,
            current_question_num=submission.question_number + 1
        )
        
        return AnswerEvaluation(score=score, feedback=feedback)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{settings.API_PREFIX}/interview/results/{{session_id}}", response_model=InterviewResults)
async def get_results(session_id: str):
    """Get interview results"""
    try:
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        qa_pairs = session_manager.get_qa_pairs(session_id)
        
        if not qa_pairs:
            raise HTTPException(status_code=400, detail="No answers submitted")
        
        # Calculate final score
        total_score = sum(qa.score for qa in qa_pairs)
        avg_score = total_score / len(qa_pairs)
        percentage = (avg_score / 10) * 100
        
        return InterviewResults(
            session_id=session_id,
            candidate_name=session.candidate_name,
            job_title=session.job_title,
            interview_type=session.interview_type,
            final_score=avg_score,
            percentage=percentage,
            qa_pairs=qa_pairs,
            start_time=session.start_time,
            completed_at=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Database endpoints
@app.post(f"{settings.API_PREFIX}/interview/save/{{session_id}}")
async def save_interview(session_id: str):
    """Save interview to database"""
    try:
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        qa_pairs = session_manager.get_qa_pairs(session_id)
        
        if not qa_pairs:
            raise HTTPException(status_code=400, detail="No answers to save")
        
        # Calculate final score
        total_score = sum(qa.score for qa in qa_pairs)
        avg_score = total_score / len(qa_pairs)
        
        # Prepare data for database
        interview_data = {
            'candidate_name': session.candidate_name,
            'job_title': session.job_title,
            'interview_type': session.interview_type,
            'final_score': avg_score,
            'start_time': session.start_time.isoformat(),
            'qa_pairs': [qa.dict() for qa in qa_pairs]
        }
        
        interview_id = db_service.save_interview(interview_data)
        
        if not interview_id:
            raise HTTPException(status_code=500, detail="Failed to save interview")
        
        # Clean up session
        session_manager.delete_session(session_id)
        
        return {"interview_id": interview_id, "success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{settings.API_PREFIX}/interviews")
async def get_all_interviews():
    """Get all interviews from database"""
    try:
        interviews = db_service.get_all_interviews()
        return {"interviews": interviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{settings.API_PREFIX}/interviews/{{interview_id}}")
async def get_interview_details(interview_id: str):
    """Get interview details by ID"""
    try:
        interview = db_service.get_interview_by_id(interview_id)
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        questions = db_service.get_questions(interview_id)
        
        return {
            "interview": interview,
            "questions": questions
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Audio endpoints
@app.post(f"{settings.API_PREFIX}/audio/tts")
async def text_to_speech(request: TTSRequest):
    """Convert text to speech"""
    try:
        audio_content = openai_service.text_to_speech(request.text)
        return StreamingResponse(
            io.BytesIO(audio_content),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(f"{settings.API_PREFIX}/audio/stt", response_model=AudioResponse)
async def speech_to_text(audio: UploadFile = File(...)):
    """Convert speech to text"""
    try:
        # Read audio file
        audio_content = await audio.read()
        
        # Create file-like object
        audio_file = io.BytesIO(audio_content)
        audio_file.name = "audio.wav"
        
        # Transcribe
        transcription = openai_service.speech_to_text(audio_file)
        
        return AudioResponse(success=True, data=transcription)
    except Exception as e:
        return AudioResponse(success=False, error=str(e))

@app.get(f"{settings.API_PREFIX}/config")
async def get_config():
    """Get frontend configuration"""
    return {
        "total_questions": settings.DEFAULT_TOTAL_QUESTIONS,
        "repeat_window_seconds": settings.REPEAT_WINDOW_SECONDS,
        "record_max_time_seconds": settings.RECORD_MAX_TIME_SECONDS,
        "stop_button_time_seconds": settings.STOP_BUTTON_TIME_SECONDS,
        "preview_time_seconds": settings.PREVIEW_TIME_SECONDS
    }

# Database schema endpoint
@app.get(f"{settings.API_PREFIX}/database/schema")
async def get_database_schema():
    """Get database schema SQL"""
    return {"schema": db_service.get_table_schema()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
