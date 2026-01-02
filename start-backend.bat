@echo off
REM Start Backend Server

echo 🚀 Starting AI Interview Backend...

cd backend

if not exist venv (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    exit /b 1
)

call venv\Scripts\activate.bat

echo ✅ Starting server on http://localhost:8000
python -m backend.main
