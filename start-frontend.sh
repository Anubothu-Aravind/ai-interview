#!/bin/bash

# Start Frontend Development Server

echo "🎨 Starting AI Interview Frontend..."

cd frontend

if [ ! -d "node_modules" ]; then
    echo "❌ Dependencies not installed. Please run setup.sh first."
    exit 1
fi

echo "✅ Starting development server on http://localhost:3000"
npm start
