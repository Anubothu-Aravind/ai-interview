# AI Interview System

A comprehensive AI-powered interview platform with separate **React.js Frontend** and **Python Backend** that conducts technical and HR interviews using resume and job description analysis, voice-based interaction, automated scoring, and interview history tracking.

## 🏗️ Architecture

- **Frontend**: React.js with TypeScript
- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **AI**: OpenAI GPT-4 for questions & evaluation, Whisper for STT, TTS-1 for voice

## ✨ Features

### 🔹 Interview Setup
- Candidate name, job role, interview type (HR / Technical)
- Resume upload (PDF / TXT)
- Job description upload (PDF / TXT)
- Fixed number of interview questions (10)

### 🔹 AI-Generated Interview Questions
- Questions generated from resume and job description
- Different question styles for HR and Technical interviews
- Questions adapt based on previous answers

### 🔹 Voice-Based Question Delivery
- Questions are read aloud automatically
- Audio playback completes fully before moving forward
- Clear visual indicator while audio is playing

### 🔹 Question Repeat Control
- Auto-read does not count as a repeat
- Question can be repeated a maximum of 2 times
- Repeat window is time-limited (2 minutes)
- Repeat button disables after limit is reached

### 🔹 Wait & Skip Controls
- Configurable wait time before recording starts
- Automatic transition after repeat window
- Countdown before recording begins

### 🔹 Timed Voice Answer Recording
- Countdown before recording begins (3 seconds)
- Fixed maximum answer duration (5 minutes)
- Visible recording timer
- Automatic stop when time expires

### 🔹 Live Speech-to-Text Transcription
- Partial transcription shown while speaking
- Transcription updates periodically
- Read-only transcription (cannot be edited)

### 🔹 Answer Submission
- Manual "Stop & Submit" button after minimum time (90 seconds)
- Automatic submission when time limit is reached

### 🔹 AI-Based Answer Evaluation
- Score assigned for each answer (0–10)
- Evaluation based on relevance, clarity, and correctness
- Separate evaluation logic for HR and Technical interviews
- Written feedback provided per answer

### 🔹 Interview Results & Feedback
- Overall interview score
- Question-wise score breakdown
- Detailed feedback for each answer
- Save results to database

### 🔹 Interview History
- View past interviews
- Access previous scores and feedback
- Detailed Q&A history for each interview

### 🔹 System Status & Reliability
- Real-time system status indicators
- Safe handling of audio and timing
- Responsive UI design
- Error handling and user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 16+
- OpenAI API Key
- Supabase account

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file in project root:
```bash
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_key
```

4. Set up database tables in Supabase SQL Editor:
```bash
# Get the schema by running the backend and visiting:
# http://localhost:8000/api/v1/database/schema
```

5. Start the backend server:
```bash
python -m backend.main
# Or with uvicorn:
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
REACT_APP_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## 📁 Project Structure

```
ai-interview/
├── backend/                 # FastAPI backend
│   ├── main.py             # FastAPI app & routes
│   ├── config.py           # Configuration
│   ├── models.py           # Pydantic models
│   ├── database.py         # Database service
│   ├── openai_service.py   # OpenAI integration
│   ├── session_manager.py  # Session management
│   ├── utils.py            # Utilities
│   ├── requirements.txt    # Python dependencies
│   └── README.md
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── types/         # TypeScript types
│   │   ├── utils/         # Utility functions
│   │   ├── styles/        # CSS files
│   │   └── App.tsx        # Main app
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── app/                    # Legacy Streamlit app (deprecated)
├── main.py                 # Legacy entry point (deprecated)
├── .env                    # Environment variables
├── .gitignore
└── README.md
```

## 🔧 API Endpoints

### Health & Config
- `GET /health` - System health check
- `GET /api/v1/config` - Get configuration

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

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## 📦 Production Build

### Backend
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run with gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm run build
# Serve the build folder with your preferred server
```

## 🔒 Security Notes

- Never commit `.env` files
- Use environment variables for sensitive data
- Enable CORS only for trusted origins in production
- Use HTTPS in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions, please open an issue on GitHub.

