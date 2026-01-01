# AI Interview Backend

FastAPI-based backend for the AI Interview System.

## Features

- RESTful API for interview management
- File upload (PDF/TXT) for resumes and job descriptions
- OpenAI integration for question generation and answer evaluation
- Text-to-Speech (TTS) and Speech-to-Text (STT) endpoints
- Supabase database integration
- Session management for active interviews

## Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create `.env` file in the project root with:
```
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_key
```

3. Run the server:
```bash
python -m backend.main
```

Or with uvicorn:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
- `GET /health` - Check API health status

### File Upload
- `POST /api/v1/upload/pdf` - Upload PDF file
- `POST /api/v1/upload/txt` - Upload TXT file

### Interview Management
- `POST /api/v1/interview/start` - Start new interview
- `POST /api/v1/interview/question` - Get next question
- `POST /api/v1/interview/answer` - Submit answer
- `GET /api/v1/interview/results/{session_id}` - Get results
- `POST /api/v1/interview/save/{session_id}` - Save to database

### Interview History
- `GET /api/v1/interviews` - Get all interviews
- `GET /api/v1/interviews/{interview_id}` - Get interview details

### Audio
- `POST /api/v1/audio/tts` - Text to speech
- `POST /api/v1/audio/stt` - Speech to text

### Configuration
- `GET /api/v1/config` - Get configuration
- `GET /api/v1/database/schema` - Get database schema

## Database Schema

Run the SQL schema from `/api/v1/database/schema` endpoint in your Supabase SQL editor to create the required tables.
