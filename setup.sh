#!/bin/bash

# AI Interview System - Quick Setup Script
# This script sets up both backend and frontend

set -e

echo "🚀 Setting up AI Interview System..."
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.12+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Setup environment files
echo "📝 Setting up environment files..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Created .env file from .env.example"
    echo "⚠️  Please edit .env and add your API keys before running the services!"
else
    echo "✅ .env file already exists"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo "✅ Created frontend/.env file"
else
    echo "✅ frontend/.env file already exists"
fi

echo ""

# Setup backend
echo "🔧 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete"
cd ..

echo ""

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend

echo "Installing frontend dependencies..."
npm install

echo "✅ Frontend setup complete"
cd ..

echo ""
echo "✨ Setup complete!"
echo ""
echo "📌 Next steps:"
echo "1. Edit .env file with your OpenAI and Supabase credentials"
echo "2. Set up database tables in Supabase (see DEPLOYMENT.md)"
echo "3. Start backend: cd backend && source venv/bin/activate && python -m backend.main"
echo "4. Start frontend (in new terminal): cd frontend && npm start"
echo ""
echo "📚 For more information, see README.md"
