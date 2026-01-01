# AI Interview System - Repository Analysis

## Executive Summary

This repository contains an AI-powered interview platform built with Streamlit that conducts technical and HR interviews using OpenAI's GPT-4 and Whisper models. The system analyzes candidate resumes and job descriptions to generate contextual questions, supports voice/text input, provides automated scoring with AI-powered feedback, and maintains interview history in a Supabase database.

## Repository Structure

```
ai-interview/
│
├── main.py                 # Streamlit entry point
├── app/
│   ├── __init__.py         # Module initialization
│   ├── config.py           # Page config, CSS, env loading
│   ├── state.py            # Session state initialization
│   ├── database.py         # Supabase DB manager
│   ├── openai_client.py    # OpenAI init + AI functions
│   ├── audio.py            # TTS / STT helpers (OpenAI Whisper & TTS)
│   ├── utils.py            # PDF extraction utilities
│   ├── ui.py               # UI components (setup, interview, results)
│   ├── history.py          # Interview history screen
│   └── app.py              # DEPRECATED: Monolithic version (kept for reference)
│
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Python dependencies (legacy)
├── uv.lock                 # UV package manager lock file
├── .gitignore              # Git ignore patterns
└── README.md               # Project documentation
```

## Technology Stack

### Core Technologies

1. **Frontend Framework**: Streamlit 1.52.2
   - Interactive web UI for interview platform
   - Real-time audio visualization
   - Session state management

2. **Backend & APIs**:
   - **OpenAI GPT-4**: Question generation and answer evaluation
   - **OpenAI Whisper**: Speech-to-text transcription
   - **OpenAI TTS**: Text-to-speech for question narration
   - **Supabase**: PostgreSQL database for interview persistence

3. **Audio Processing**:
   - `sounddevice`: Real-time audio recording
   - `scipy`: Audio file handling (WAV format)
   - `numpy`: Audio data manipulation
   - `matplotlib`: Waveform visualization

4. **Document Processing**:
   - `PyPDF2`: PDF text extraction for resumes and job descriptions
   - `python-dotenv`: Environment variable management

5. **Data & Visualization**:
   - `plotly`: Interactive charts (available but not actively used)
   - `pandas`: Data manipulation (available but not actively used)

### Dependencies

Full dependency list from `pyproject.toml`:
- anthropic>=0.75.0 (unused, likely for future features)
- gtts>=2.5.4 (deprecated, replaced by OpenAI TTS)
- matplotlib>=3.10.8
- numpy>=2.4.0
- openai>=2.14.0
- pandas>=2.3.3
- plotly>=6.5.0
- psycopg2-binary>=2.9.11 (unused, direct DB access not implemented)
- pyaudio>=0.2.14 (available but using sounddevice)
- pydub>=0.25.1 (available but not actively used)
- pypdf2>=3.0.1
- python-dotenv>=1.2.1
- scipy>=1.16.3
- sounddevice>=0.5.3
- speechrecognition>=3.14.4 (deprecated, replaced by OpenAI Whisper)
- streamlit>=1.52.2
- supabase>=2.27.0

## System Architecture

### Application Flow

1. **Initialization** (`main.py`):
   - Load configuration and environment variables
   - Initialize session state
   - Connect to Supabase and OpenAI
   - Render the application UI

2. **Interview Setup** (`ui.py:render_setup`):
   - Collect candidate information (name, job title)
   - Upload resume and job description (PDF/TXT)
   - Select interview type (technical/hr)
   - Generate first AI question

3. **Interview Execution** (`ui.py:render_interview`):
   - Display question with progress indicator
   - Auto-play question via TTS (OpenAI)
   - Allow question repeat (120-second window)
   - Record candidate's audio answer (300-second max)
   - Live waveform visualization
   - Partial transcription preview (every 5 seconds)
   - Full transcription on completion
   - AI-powered answer evaluation (score + feedback)
   - Generate next contextual question

4. **Results & Persistence** (`ui.py:render_results`):
   - Calculate overall score
   - Display detailed Q&A with feedback
   - Save to Supabase database
   - View past interview history

### Key Components

#### 1. Configuration (`app/config.py`)
- Streamlit page configuration
- Custom CSS for UI styling
- Environment variable loading via dotenv

#### 2. Session State (`app/state.py`)
Manages interview flow state:
- Interview progress tracking
- Question timing and controls
- Recording state management
- Audio data buffering
- User preferences (HR vs Technical mode)

#### 3. Database Layer (`app/database.py`)
- Supabase client initialization with caching
- `DatabaseManager` class for CRUD operations
- Two-table schema:
  - `interviews`: Main interview records
  - `questions`: Individual Q&A pairs (foreign key to interviews)
- Automatic cascade deletion

#### 4. OpenAI Integration (`app/openai_client.py`)
- **Question Generation**: Context-aware question creation using:
  - Resume content
  - Job description requirements
  - Interview type (technical/hr)
  - Conversation history for contextual follow-ups
- **Answer Evaluation**: JSON-formatted scoring (0-10) with constructive feedback

#### 5. Audio Processing (`app/audio.py`)
- **Text-to-Speech**: OpenAI TTS with "alloy" voice
- **Recording Pipeline**:
  - 16kHz sample rate
  - 1-second chunks for real-time visualization
  - Continuous accumulation in session state
- **Transcription**:
  - Partial: Every 5 seconds during recording
  - Final: On recording completion
  - Float32 to Int16 conversion for WAV format
- **Waveform Visualization**: Matplotlib real-time plotting

#### 6. UI Components (`app/ui.py`)
Modular rendering functions:
- `render_sidebar`: System status and navigation
- `render_setup`: Initial interview configuration
- `render_interview`: Active interview session
- `finalize_answer`: Answer processing and evaluation
- `render_results`: Final score and detailed results
- `render_app`: Main orchestrator

#### 7. History View (`app/history.py`)
- Two-column layout: interview list + details
- Interview filtering by date (newest first)
- Detailed Q&A review with scores

## Database Schema

### Interviews Table
```sql
CREATE TABLE IF NOT EXISTS interviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    interview_type TEXT NOT NULL,
    final_score FLOAT,
    start_time TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Questions Table
```sql
CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interview_id UUID REFERENCES interviews(id) ON DELETE CASCADE,
    question_number INT,
    question_text TEXT,
    answer TEXT,
    score FLOAT,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Key Features

### 1. AI-Powered Question Generation
- Context-aware questions based on resume and JD
- Progressive difficulty (easier → harder)
- Conversation history for follow-up questions
- Separate prompts for technical vs HR interviews

### 2. Multi-Modal Input
- Text input via textarea
- Voice recording with real-time visualization
- Live transcription preview
- Automatic transcription using OpenAI Whisper

### 3. Real-Time Recording Experience
- 2-minute repeat window for question clarification
- 3-second countdown before recording starts
- Live waveform display during recording
- Partial transcription every 5 seconds
- Final 20 seconds: live transcription preview
- Manual stop button (after 90 seconds)
- Auto-stop at 5 minutes

### 4. AI Evaluation
- 0-10 scoring system
- Constructive feedback (2-3 sentences)
- Evaluation criteria:
  - Relevance to question
  - Depth of knowledge
  - Communication clarity
  - Alignment with job requirements

### 5. Interview History
- Persistent storage in Supabase
- Searchable past interviews
- Detailed review of all Q&A pairs
- Score tracking and analytics

## Code Organization & Best Practices

### Strengths
1. **Modular Architecture**: Clean separation of concerns (config, state, database, UI, audio)
2. **Type Hints**: Modern Python typing (e.g., `Client | None`)
3. **Resource Caching**: `@st.cache_resource` for expensive operations
4. **Error Handling**: Try-catch blocks with user-friendly error messages
5. **Session State Management**: Centralized state initialization
6. **Deprecation Management**: Old monolithic `app.py` kept for reference
7. **Database Safety**: Cascade deletion, proper foreign key relationships

### Code Quality Observations
1. **Good Practices**:
   - Environment variable usage for secrets
   - Temporary file cleanup in `finally` blocks
   - Progress indicators for user experience
   - Inline documentation in database schema

2. **Areas for Improvement**:
   - No unit tests or integration tests
   - Hard-coded constants (could use config file)
   - Limited error recovery mechanisms
   - No logging framework (only Streamlit messages)
   - Some unused dependencies (anthropic, gtts, speechrecognition)

## Interview Timing Configuration

Default timings (in `state.py`):
- `repeat_window`: 120 seconds (2 minutes) - Question repeat allowed
- `record_max_time`: 300 seconds (5 minutes) - Maximum recording duration
- `stop_button_time`: 90 seconds (1.5 minutes) - When stop button appears
- `preview_time`: 20 seconds - When live transcription preview shows
- `transcribe_every`: 5 seconds - Partial transcription interval

## Security Considerations

### Current Implementation
1. **Environment Variables**: API keys stored in `.env` (gitignored)
2. **Service Role Key**: Uses Supabase service role key (backend only)
3. **No User Authentication**: Anyone with access can use the system
4. **No Rate Limiting**: Potential for API abuse

### Recommendations
1. Add user authentication (Supabase Auth)
2. Implement rate limiting for OpenAI API calls
3. Add input validation for uploaded files
4. Sanitize user inputs to prevent SQL injection (though using ORM)
5. Add file size limits for uploads
6. Consider client-side key usage with Row Level Security (RLS)

## Performance Characteristics

### Bottlenecks
1. **OpenAI API Calls**: Synchronous, can take 2-5 seconds
2. **Audio Transcription**: Processes entire recording (up to 5 minutes)
3. **Database Writes**: Bulk insert of 10+ questions per interview
4. **Real-time Recording**: Streamlit reruns every second during recording

### Optimization Opportunities
1. Async OpenAI calls for faster response
2. Streaming transcription during recording
3. Database connection pooling
4. Audio compression before transcription
5. Caching of common resume/JD patterns

## Deployment Considerations

### Environment Variables Required
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
OPENAI_API_KEY=your_openai_api_key
```

### Database Setup
Run SQL schema from `DatabaseManager.create_tables()` in Supabase SQL Editor once.

### Streamlit Configuration
- Runs on default port 8501
- Requires microphone permissions for voice recording
- Wide layout, expanded sidebar by default

### Resource Requirements
- Python 3.12+
- Internet connection for OpenAI and Supabase APIs
- Microphone access for voice recording
- Adequate OpenAI API credits

## Potential Improvements

### High Priority
1. **Testing**: Add unit tests, integration tests, and E2E tests
2. **Error Recovery**: Better handling of API failures, network issues
3. **Dependency Cleanup**: Remove unused packages (anthropic, gtts, speechrecognition, pyaudio)
4. **User Authentication**: Add login/signup with Supabase Auth
5. **Input Validation**: File type, size, and content validation

### Medium Priority
1. **Analytics Dashboard**: Aggregate statistics across interviews
2. **Export Features**: PDF reports, Excel exports
3. **Resume Parsing**: Structured extraction (skills, experience, education)
4. **Question Bank**: Pre-defined question templates
5. **Multi-language Support**: i18n for global usage
6. **Email Notifications**: Send results to candidates

### Low Priority (Nice to Have)
1. **Video Recording**: Add video support for behavioral interviews
2. **Interview Scheduling**: Calendar integration
3. **Collaborative Reviews**: Multiple reviewers for one candidate
4. **AI Model Selection**: Allow GPT-3.5 vs GPT-4 choice
5. **Custom Branding**: White-label support
6. **Mobile Optimization**: Responsive design improvements

## Migration from Monolithic to Modular

The repository shows evidence of refactoring:
- **Old**: `app/app.py` - 725-line monolithic file
- **New**: Modular structure with 8 focused modules

Key differences:
1. Deprecated `gtts` → OpenAI TTS
2. Deprecated `SpeechRecognition` → OpenAI Whisper
3. Real-time waveform visualization (new)
4. Structured session state management (new)
5. Improved error handling and UX

## Conclusion

The AI Interview System is a well-structured, functional Streamlit application that effectively combines OpenAI's AI capabilities with Supabase for a complete interview platform. The modular refactoring shows good software engineering practices. The main areas for improvement are testing coverage, security hardening, and dependency optimization.

### Overall Assessment
- **Code Quality**: ⭐⭐⭐⭐☆ (4/5) - Clean, modular, well-organized
- **Feature Completeness**: ⭐⭐⭐⭐☆ (4/5) - Core features work well
- **Scalability**: ⭐⭐⭐☆☆ (3/5) - Single-user focused, needs auth
- **Documentation**: ⭐⭐⭐☆☆ (3/5) - Good README, inline comments sparse
- **Testing**: ⭐☆☆☆☆ (1/5) - No test infrastructure

### Recommended Next Steps
1. Add comprehensive test suite
2. Implement user authentication
3. Clean up unused dependencies
4. Add logging framework
5. Create deployment documentation
6. Add API rate limiting and error recovery
