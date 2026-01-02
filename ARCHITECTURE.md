# Architecture Overview

## System Architecture

The AI Interview System is built with a modern, decoupled architecture separating frontend and backend concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│                    (React + TypeScript)                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Setup    │  │ Interview  │  │  Results   │           │
│  │   Form     │  │   Flow     │  │  Display   │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│         │               │               │                   │
│         └───────────────┴───────────────┘                   │
│                         │                                   │
│                 ┌───────▼───────┐                          │
│                 │  API Service  │                          │
│                 │   (Axios)     │                          │
│                 └───────┬───────┘                          │
└─────────────────────────┼─────────────────────────────────┘
                          │ HTTP/REST
                          │
┌─────────────────────────▼─────────────────────────────────┐
│                        Backend                             │
│                  (FastAPI + Python)                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │  FastAPI   │  │  Session   │  │  Database  │          │
│  │  Routes    │  │  Manager   │  │  Service   │          │
│  └────┬───────┘  └─────┬──────┘  └─────┬──────┘          │
│       │                │               │                   │
│  ┌────▼────────────────▼───────────────▼──────┐           │
│  │         Business Logic Layer                │           │
│  │  - File Processing                          │           │
│  │  - Question Generation                      │           │
│  │  - Answer Evaluation                        │           │
│  │  - Audio Processing                         │           │
│  └────┬────────────────┬───────────────┬───────┘           │
└───────┼────────────────┼───────────────┼───────────────────┘
        │                │               │
   ┌────▼────┐      ┌───▼────┐     ┌───▼────┐
   │ OpenAI  │      │ OpenAI │     │Supabase│
   │  GPT-4  │      │Whisper │     │   DB   │
   │   API   │      │  TTS   │     │        │
   └─────────┘      └────────┘     └────────┘
```

## Technology Stack

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: CSS3
- **Audio**: MediaRecorder API, Web Audio API
- **Build Tool**: Create React App

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.12
- **Database ORM**: Supabase Python Client
- **AI Integration**: OpenAI Python SDK
- **File Processing**: PyPDF2
- **Validation**: Pydantic v2
- **Server**: Uvicorn (ASGI)

### External Services
- **Database**: Supabase (PostgreSQL)
- **AI**: OpenAI GPT-4, Whisper, TTS-1
- **Deployment**: Flexible (Vercel, Heroku, AWS, etc.)

## Data Flow

### Interview Session Flow

1. **Setup Phase**
   ```
   User Input → File Upload → Text Extraction → Session Creation
   ```

2. **Question Generation**
   ```
   Resume + JD + History → OpenAI GPT-4 → Question Text → TTS → Audio
   ```

3. **Answer Recording**
   ```
   Microphone → MediaRecorder → Audio Blob → STT (Whisper) → Text
   ```

4. **Evaluation**
   ```
   Question + Answer + JD → OpenAI GPT-4 → Score + Feedback
   ```

5. **Results**
   ```
   All Q&A Pairs → Calculate Metrics → Display Results → Save to DB
   ```

## API Endpoints

### Health & Config
- `GET /health` - System status
- `GET /api/v1/config` - Configuration

### File Upload
- `POST /api/v1/upload/pdf` - Upload PDF
- `POST /api/v1/upload/txt` - Upload text file

### Interview Management
- `POST /api/v1/interview/start` - Initialize session
- `POST /api/v1/interview/question` - Get question
- `POST /api/v1/interview/answer` - Submit answer
- `GET /api/v1/interview/results/{id}` - Get results
- `POST /api/v1/interview/save/{id}` - Save to DB

### History
- `GET /api/v1/interviews` - List all
- `GET /api/v1/interviews/{id}` - Get details

### Audio
- `POST /api/v1/audio/tts` - Text to speech
- `POST /api/v1/audio/stt` - Speech to text

## Database Schema

### interviews
- `id` (UUID, PK)
- `candidate_name` (TEXT)
- `job_title` (TEXT)
- `interview_type` (TEXT)
- `final_score` (FLOAT)
- `start_time` (TIMESTAMP)
- `completed_at` (TIMESTAMP)
- `created_at` (TIMESTAMP)

### questions
- `id` (UUID, PK)
- `interview_id` (UUID, FK → interviews)
- `question_number` (INT)
- `question_text` (TEXT)
- `answer` (TEXT)
- `score` (FLOAT)
- `feedback` (TEXT)
- `created_at` (TIMESTAMP)

## Security Considerations

### Backend
- CORS configured for trusted origins only
- Environment variables for sensitive data
- Input validation with Pydantic
- File upload size limits
- Session-based state management

### Frontend
- API key never exposed to client
- HTTPS in production
- Input sanitization
- Secure file upload handling
- XSS protection

### Database
- Row-level security (RLS) policies
- Prepared statements (via Supabase)
- Regular backups
- Access logging

## Scalability

### Horizontal Scaling
- Backend: Multiple Uvicorn workers
- Frontend: CDN distribution
- Database: Supabase handles scaling

### Performance Optimization
- Connection pooling
- Caching for static content
- Lazy loading components
- Code splitting
- Image optimization

### Cost Management
- OpenAI API usage monitoring
- Database query optimization
- Efficient session cleanup
- CDN for static assets

## Deployment Options

### Development
- Backend: Local Uvicorn server
- Frontend: React dev server
- Database: Supabase cloud

### Production
- Backend: VPS, Heroku, Railway, Render
- Frontend: Vercel, Netlify, S3+CloudFront
- Database: Supabase production tier

## Monitoring & Logging

### Application Monitoring
- Error tracking (Sentry)
- Performance monitoring (APM)
- User analytics
- API usage tracking

### Infrastructure Monitoring
- Server health checks
- Database metrics
- API response times
- Resource utilization

## Future Enhancements

### Features
- Video recording support
- Multi-language interviews
- Custom question banks
- Interview scheduling
- Email notifications
- Advanced analytics
- Team collaboration
- Mobile app

### Technical Improvements
- WebSocket for real-time features
- Redis caching
- GraphQL API option
- Microservices architecture
- Kubernetes deployment
- CI/CD pipeline
- Automated testing
- Load balancing

## Development Workflow

1. **Local Development**
   - Run setup scripts
   - Start backend and frontend
   - Use local Supabase or cloud

2. **Feature Development**
   - Create feature branch
   - Implement changes
   - Test locally
   - Submit PR

3. **Code Review**
   - Automated checks
   - Manual review
   - Merge to main

4. **Deployment**
   - Automated via CI/CD
   - Staging first
   - Production after approval

## Support & Maintenance

- Regular dependency updates
- Security patches
- Performance optimization
- Bug fixes
- Feature requests
- Documentation updates
# System Architecture Documentation

## Overview

This document provides a detailed technical architecture of the AI Interview System, including component interactions, data flow, and integration patterns.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Streamlit Web UI                         │
│  (User Interface Layer - main.py, app/ui.py, app/history.py)   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────────┐
│                    Application Layer (app/)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   config.py  │  │   state.py   │  │   utils.py   │          │
│  │ (Config/CSS) │  │ (State Mgmt) │  │ (PDF Utils)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────────┐
│                    Service Layer (app/)                          │
│  ┌──────────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│  │  database.py     │  │ openai_client.py│  │   audio.py     │ │
│  │ (DB Operations)  │  │ (AI Services)   │  │ (Audio I/O)    │ │
│  └────────┬─────────┘  └────────┬────────┘  └────────┬───────┘ │
└───────────┼────────────────────┼──────────────────────┼─────────┘
            │                    │                      │
            │                    │                      │
┌───────────┴─────────┐  ┌───────┴──────────┐  ┌───────┴─────────┐
│  Supabase (Cloud)   │  │  OpenAI API      │  │  Local Audio    │
│  - PostgreSQL DB    │  │  - GPT-4         │  │  - Microphone   │
│  - REST API         │  │  - Whisper STT   │  │  - Sounddevice  │
│                     │  │  - TTS           │  │                 │
└─────────────────────┘  └──────────────────┘  └─────────────────┘
```

## Component Details

### 1. Entry Point (`main.py`)

**Responsibilities**:
- Bootstrap the application
- Load environment configuration
- Initialize global resources (Supabase, OpenAI clients)
- Launch Streamlit app

**Flow**:
```python
main()
  ├── load_config()              # Load .env, set page config, inject CSS
  ├── init_session_state()       # Initialize Streamlit session variables
  ├── init_supabase()            # Connect to Supabase (cached)
  ├── init_openai()              # Initialize OpenAI client (cached)
  └── render_app(db, client)     # Start UI rendering loop
```

### 2. Configuration Module (`app/config.py`)

**Purpose**: Centralized configuration and styling

**Functions**:
- `load_config()`: 
  - Loads `.env` file via `python-dotenv`
  - Sets Streamlit page configuration
  - Injects custom CSS for gradient headers and styled boxes

**CSS Classes**:
- `.main-header`: Gradient text header
- `.question-box`: Purple gradient question container

### 3. State Management (`app/state.py`)

**Purpose**: Initialize and manage session state

**Key State Variables**:

| Variable | Type | Purpose |
|----------|------|---------|
| `interview_started` | bool | Whether interview is in progress |
| `current_question_num` | int | Current question number (1-10) |
| `current_question` | str | Question text being asked |
| `total_questions` | int | Total questions (default: 10) |
| `conversation_history` | list | Q&A pairs for context |
| `all_qa` | list | Full Q&A with scores |
| `question_spoken` | bool | Whether TTS played for current question |
| `question_start_time` | float | Timestamp when question displayed |
| `recording` | bool | Whether recording is active |
| `recording_start_time` | float | Timestamp when recording started |
| `audio_frames` | list | Accumulated audio chunks |
| `partial_transcript` | str | Live transcription preview |
| `hr_mode` | bool | HR vs Technical interview type |
| `show_history` | bool | Whether showing history view |

**Timing Parameters**:
```python
repeat_window = 120        # 2 minutes to repeat question
record_max_time = 300      # 5 minutes max recording
stop_button_time = 90      # 1.5 minutes before stop button appears
preview_time = 20          # Last 20 seconds show preview
```

### 4. Database Layer (`app/database.py`)

**Architecture**:
```
DatabaseManager
├── __init__(supabase_client)
├── create_tables() → SQL schema string
├── save_interview(data) → interview_id
├── get_all_interviews() → list[dict]
└── get_questions(interview_id) → list[dict]
```

**Data Models**:

**Interview**:
```python
{
    "id": UUID,
    "candidate_name": str,
    "job_title": str,
    "interview_type": "technical" | "hr",
    "final_score": float (0-10),
    "start_time": ISO timestamp,
    "completed_at": ISO timestamp,
    "created_at": ISO timestamp
}
```

**Question**:
```python
{
    "id": UUID,
    "interview_id": UUID (foreign key),
    "question_number": int (1-10),
    "question_text": str,
    "answer": str,
    "score": float (0-10),
    "feedback": str,
    "created_at": ISO timestamp
}
```

**Database Operations**:
1. **Save Interview**:
   - Insert into `interviews` table
   - Get generated interview ID
   - Bulk insert Q&A pairs into `questions` table
   - Transaction-like behavior via Supabase API

2. **Fetch Interviews**:
   - Query all interviews, ordered by `created_at DESC`
   - Return as list of dictionaries

3. **Fetch Questions**:
   - Query by `interview_id`
   - Order by `question_number`

### 5. OpenAI Integration (`app/openai_client.py`)

**Functions**:

#### `ask_ai_question(client, resume, jd, interview_type, q_num, history)`

**Purpose**: Generate contextual interview question

**Inputs**:
- `client`: OpenAI client instance
- `resume`: Extracted resume text
- `jd`: Job description text
- `interview_type`: "technical" or "hr"
- `q_num`: Question number (1-10)
- `history`: Previous Q&A pairs for context

**Process**:
1. Build context string from conversation history
2. Construct prompt with JD, resume, context, and interview type
3. Call GPT-4 with temperature=0.7 (creative)
4. Return question text

**Prompt Structure**:
```
Job Description:
{jd}

Resume:
{resume}

{Previous Q&A context}

Generate question {q_num}/10 for a {interview_type} interview.
```

#### `evaluate_answer(client, question, answer, jd, interview_type)`

**Purpose**: Score and provide feedback on candidate answer

**Inputs**:
- `question`: The question asked
- `answer`: Candidate's response
- `jd`: Job description
- `interview_type`: Interview type

**Output**:
```python
(score: float, feedback: str)
```

**Process**:
1. Send question and answer to GPT-4
2. Request JSON response with `score` and `feedback` fields
3. Parse JSON response
4. Return tuple

**Prompt Structure**:
```
Return JSON with exactly two fields:
score (number 0-10)
feedback (string)

Question: {question}
Answer: {answer}
```

**Model**: GPT-4 with temperature=0.5 (more deterministic for scoring)

### 6. Audio Processing (`app/audio.py`)

#### Audio Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Recording Phase                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  start_recording()                                           │
│       │                                                       │
│       ├──> Clear audio_frames[]                             │
│       └──> Clear partial_transcript                          │
│                                                               │
│  [Loop every 1 second]                                       │
│       │                                                       │
│       ├──> record_chunk()                                    │
│       │      │                                               │
│       │      ├──> Record 1 second @ 16kHz                   │
│       │      └──> Append to audio_frames[]                  │
│       │                                                       │
│       ├──> draw_waveform()                                   │
│       │      │                                               │
│       │      ├──> Concatenate all frames                    │
│       │      ├──> Plot with matplotlib                      │
│       │      └──> Display in Streamlit                      │
│       │                                                       │
│       └──> [Every 5 seconds]                                │
│              │                                               │
│              └──> transcribe_partial()                      │
│                     │                                        │
│                     ├──> Concatenate frames                 │
│                     ├──> Convert float32 → int16           │
│                     ├──> Write temp WAV file               │
│                     ├──> Call Whisper API                  │
│                     └──> Update partial_transcript         │
│                                                               │
│  [On Stop/Timeout]                                           │
│       │                                                       │
│       └──> stop_and_transcribe()                            │
│              │                                               │
│              ├──> Concatenate all frames                    │
│              ├──> Convert float32 → int16                  │
│              ├──> Write temp WAV file                      │
│              ├──> Call Whisper API                         │
│              └──> Return final transcript                  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

#### Text-to-Speech (`text_to_speech`)

**Flow**:
1. Initialize OpenAI client
2. Call `audio.speech.create()` with:
   - Model: `tts-1`
   - Voice: `alloy`
   - Input text
3. Save response to temporary MP3 file
4. Play via Streamlit's `st.audio()` with `autoplay=True`
5. Clean up temporary file

#### Audio Format Details

| Parameter | Value | Reason |
|-----------|-------|--------|
| Sample Rate | 16000 Hz | Standard for speech recognition |
| Channels | 1 (Mono) | Speech doesn't need stereo |
| Data Type | float32 | Internal sounddevice format |
| Output Format | int16 WAV | Whisper API requirement |
| Chunk Size | 1 second | Real-time visualization |

### 7. UI Components (`app/ui.py`)

#### Component Hierarchy

```
render_app (Main Orchestrator)
├── render_sidebar
│   ├── System Status (Supabase, OpenAI)
│   ├── View Past Interviews Button
│   └── Show SQL Script Button
│
├── [Route based on state]
│
├── render_history (if show_history=True)
│   ├── Interview List (Column 1)
│   └── Interview Details (Column 2)
│       ├── Metadata
│       └── Q&A Expanders
│
├── render_setup (if not interview_started)
│   ├── Candidate Info Form
│   │   ├── Name
│   │   ├── Job Title
│   │   └── Interview Type
│   ├── File Uploads
│   │   ├── Resume (PDF/TXT)
│   │   └── Job Description (PDF/TXT)
│   └── Start Button
│       └── [Generates first question]
│
├── render_interview (if interview_started and not complete)
│   ├── Progress Bar
│   ├── Question Display
│   ├── Auto TTS Playback (once)
│   ├── Repeat Button (2-minute window)
│   ├── Recording Phase
│   │   ├── Live Waveform
│   │   ├── Partial Transcription (every 5s)
│   │   ├── Preview (last 20s)
│   │   └── Stop Button (after 90s)
│   └── [Auto proceed to next or finalize]
│
└── render_results (if interview complete)
    ├── Overall Score
    ├── Q&A Expanders
    ├── Save to Database Button
    └── Download JSON Button (unused currently)
```

#### Interview Flow State Machine

```
[SETUP] → [INTERVIEW] → [RESULTS]
   │           │             │
   │           │             └──> Save & History
   │           │
   │           └──> For each question (1-10):
   │                   ├─> Display Question
   │                   ├─> Auto TTS
   │                   ├─> Repeat Window (0-120s)
   │                   ├─> Recording Phase (120-420s)
   │                   │    ├─> Live Recording (1s chunks)
   │                   │    ├─> Waveform Update
   │                   │    ├─> Partial Transcription (every 5s)
   │                   │    └─> Stop (manual or 300s timeout)
   │                   ├─> Final Transcription
   │                   ├─> AI Evaluation
   │                   └─> Next Question
   │
   └──> Extract Resume & JD → Generate Q1
```

### 8. History View (`app/history.py`)

**Layout**: Two-column interface

**Column 1**: Interview List
- Button for each past interview
- Format: `{name} | {job} | {date}`
- Click to select

**Column 2**: Interview Details
- Metadata display
- Questions with expandable answers
- Score and feedback for each Q&A

## Data Flow Diagrams

### Interview Setup Flow

```
User Input → File Upload → Text Extraction → AI Question Generation → Session State
     │             │              │                    │                    │
     │             │              │                    │                    │
  Form Data    PDF/TXT       PyPDF2/read         GPT-4 API         st.session_state
     │             │              │                    │                    │
     └─────────────┴──────────────┴────────────────────┴────────────────────┘
                                   │
                                   ▼
                           interview_started = True
```

### Recording & Evaluation Flow

```
Question Display → TTS Playback → Recording → Transcription → Evaluation → Next Question
       │               │             │            │              │              │
       │               │             │            │              │              │
  st.markdown()   OpenAI TTS    sounddevice   Whisper API    GPT-4 API    ask_ai_question()
       │               │             │            │              │              │
       │               │             │            │              │              │
    Display         autoplay     audio_frames   transcript   score/feedback   Q(n+1)
```

### Database Persistence Flow

```
Interview Complete → Format Data → Save Interview → Save Questions → Confirmation
        │                │              │               │                │
        │                │              │               │                │
    all_qa[]      interview_data   INSERT INTO    INSERT INTO      Success Message
        │                │          interviews     questions             │
        │                │              │               │                │
        └────────────────┴──────────────┴───────────────┴────────────────┘
                                        │
                                        ▼
                                 Supabase Storage
```

## Integration Points

### 1. OpenAI API Integration

**Endpoints Used**:
- `chat.completions.create` - GPT-4 for Q&A
- `audio.speech.create` - TTS for questions
- `audio.transcriptions.create` - Whisper for STT

**Authentication**: Bearer token via `OPENAI_API_KEY`

**Error Handling**:
- Fallback default questions on API failure
- Default score (7/10) on evaluation failure
- User-facing error messages via `st.error()`

### 2. Supabase Integration

**Client Library**: `supabase-py`

**Authentication**: Service role key (full access)

**Tables**: `interviews`, `questions`

**Operations**:
- `.insert()` - Create records
- `.select()` - Query records
- `.eq()` - Filter by field
- `.order()` - Sort results

**Connection**: 
- Cached via `@st.cache_resource`
- Configurable timeouts (30s)

### 3. Local Audio Device Integration

**Library**: `sounddevice`

**Operations**:
- `sd.rec()` - Record audio chunk
- `sd.wait()` - Block until recording complete

**Device**: Default system microphone

**Format**: 1-channel, 16kHz, float32

## Security Architecture

### Current State

**Secrets Management**:
- `.env` file (git-ignored)
- Environment variables loaded at runtime
- No secrets in code

**Access Control**:
- No user authentication
- Service role key used (full DB access)
- Open API usage (anyone with app access)

**Input Validation**:
- File type checking (PDF/TXT)
- No file size limits
- No content sanitization

### Recommended Security Enhancements

1. **Authentication**: Add Supabase Auth with RLS
2. **Authorization**: Implement role-based access
3. **Rate Limiting**: Throttle OpenAI API calls
4. **Input Validation**: 
   - File size limits
   - Content sanitization
   - Malicious PDF detection
5. **Audit Logging**: Track all API calls and DB operations
6. **Encryption**: Encrypt sensitive data at rest

## Scalability Considerations

### Current Limitations

1. **Single-user Sessions**: Streamlit session-based, no multi-tenancy
2. **Synchronous API Calls**: Blocking operations during AI calls
3. **No Caching**: Every interview generates new questions
4. **Memory Storage**: Audio frames held in session state
5. **No Queue System**: Sequential processing only

### Scaling Recommendations

1. **Horizontal Scaling**:
   - Deploy multiple Streamlit instances
   - Use load balancer
   - Session affinity required

2. **Performance Optimizations**:
   - Async OpenAI calls
   - Background job processing for transcription
   - Redis caching for common patterns
   - CDN for static assets

3. **Database Optimization**:
   - Connection pooling
   - Indexed queries (interview_id, created_at)
   - Archival strategy for old interviews

4. **Cost Optimization**:
   - Use GPT-3.5 for less critical tasks
   - Batch API requests where possible
   - Implement usage quotas per user

## Technology Decisions & Rationale

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| Streamlit | Rapid prototyping, Python-native, built-in UI components | Limited customization, session-based architecture |
| OpenAI GPT-4 | Best-in-class AI for question generation and evaluation | Cost, latency, API dependency |
| OpenAI Whisper | Accurate speech-to-text, same provider as GPT-4 | Latency, processing time for long audio |
| Supabase | PostgreSQL + REST API, easy setup, generous free tier | Vendor lock-in, limited to PostgreSQL features |
| sounddevice | Cross-platform audio I/O, NumPy integration | Requires PortAudio system library |
| PyPDF2 | Simple PDF parsing, pure Python | Limited formatting support, no OCR |
| Modular structure | Maintainability, testability, separation of concerns | More files, import overhead |

## Future Architecture Considerations

### Microservices Migration Path

```
Current Monolith → Hybrid → Full Microservices
       │              │              │
       │              │              ├─> API Gateway
       │              │              ├─> Auth Service
       │              │              ├─> Interview Service
       │              ├─> Add API   ├─> AI Service
       │              └─> layer      ├─> Storage Service
       │                              └─> Notification Service
       │
       └─> Current State (Single Streamlit App)
```

### Event-Driven Architecture

Potential event flow:
```
Interview Started → Question Generated → Answer Recorded → 
  ↓                    ↓                    ↓
Event Bus          Event Bus          Event Bus
  ↓                    ↓                    ↓
Analytics         Cache Service      Transcription Worker
  ↓                                         ↓
Dashboard                              Evaluation Worker
                                            ↓
                                       Database Writer
```

## Conclusion

The current architecture is well-suited for a MVP/prototype with moderate usage. The modular design provides a solid foundation for future enhancements. Key architectural improvements should focus on:

1. Adding authentication and authorization
2. Implementing asynchronous processing
3. Adding comprehensive error handling and logging
4. Optimizing for concurrent users
5. Implementing caching strategies

The choice of Streamlit makes the application accessible and easy to deploy but may require migration to a more scalable framework (FastAPI + React) for production use at scale.
