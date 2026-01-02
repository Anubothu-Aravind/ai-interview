@echo off
REM Start Frontend Development Server

echo 🎨 Starting AI Interview Frontend...

cd frontend

if not exist node_modules (
    echo ❌ Dependencies not installed. Please run setup.bat first.
    exit /b 1
)

echo ✅ Starting development server on http://localhost:3000
npm start
