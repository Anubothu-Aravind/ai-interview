@echo off
REM AI Interview System - Quick Setup Script for Windows
REM This script sets up both backend and frontend

echo 🚀 Setting up AI Interview System...
echo.

REM Check prerequisites
echo 📋 Checking prerequisites...

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python 3 is not installed. Please install Python 3.12+
    exit /b 1
)

where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+
    exit /b 1
)

where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ npm is not installed. Please install npm
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Setup environment files
echo 📝 Setting up environment files...

if not exist .env (
    copy .env.example .env
    echo ⚠️  Created .env file from .env.example
    echo ⚠️  Please edit .env and add your API keys before running the services!
) else (
    echo ✅ .env file already exists
)

if not exist frontend\.env (
    copy frontend\.env.example frontend\.env
    echo ✅ Created frontend\.env file
) else (
    echo ✅ frontend\.env file already exists
)

echo.

REM Setup backend
echo 🔧 Setting up backend...
cd backend

if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r requirements.txt

echo ✅ Backend setup complete
cd ..

echo.

REM Setup frontend
echo 🎨 Setting up frontend...
cd frontend

echo Installing frontend dependencies...
call npm install

echo ✅ Frontend setup complete
cd ..

echo.
echo ✨ Setup complete!
echo.
echo 📌 Next steps:
echo 1. Edit .env file with your OpenAI and Supabase credentials
echo 2. Set up database tables in Supabase (see DEPLOYMENT.md)
echo 3. Start backend: cd backend && venv\Scripts\activate && python -m backend.main
echo 4. Start frontend (in new terminal): cd frontend && npm start
echo.
echo 📚 For more information, see README.md
pause
