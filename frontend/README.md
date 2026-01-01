# AI Interview Frontend

React TypeScript frontend for the AI Interview System.

## Features

- Modern React with TypeScript
- React Router for navigation
- Interview setup with file uploads
- Voice-based question delivery with auto-play
- Question repeat control (max 2 times, time-limited)
- Timed voice recording with live transcription
- Real-time answer evaluation display
- Interview results with detailed feedback
- Interview history browser
- Responsive design
- System status indicators

## Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

3. Update the `.env` file with your backend URL:
```
REACT_APP_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/       # React components
│   │   ├── InterviewSetup.tsx
│   │   ├── InterviewQuestion.tsx
│   │   ├── Results.tsx
│   │   └── History.tsx
│   ├── pages/           # Page components
│   │   └── InterviewPage.tsx
│   ├── services/        # API services
│   │   └── api.ts
│   ├── types/           # TypeScript types
│   │   └── index.ts
│   ├── utils/           # Utility functions
│   │   └── audio.ts
│   ├── styles/          # CSS files
│   ├── App.tsx          # Main app component
│   └── index.tsx        # Entry point
├── package.json
└── tsconfig.json
```

## Technologies Used

- React 18
- TypeScript
- React Router v6
- Axios for API calls
- MediaRecorder API for audio recording
- CSS3 for styling

## Browser Compatibility

- Chrome/Edge (recommended for best audio support)
- Firefox
- Safari (may have limited MediaRecorder support)
