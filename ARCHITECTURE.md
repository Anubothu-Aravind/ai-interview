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
