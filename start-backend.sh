#!/bin/bash

# Start Backend Server

echo "🚀 Starting AI Interview Backend..."

cd backend

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

source venv/bin/activate

echo "✅ Starting server on http://localhost:8000"
python -m backend.main
