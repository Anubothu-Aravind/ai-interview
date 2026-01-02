import React, { useState, useEffect, useRef } from 'react';
import { apiService } from '../services/api';
import { AudioRecorder, playAudioBlob, formatTime } from '../utils/audio';
import { AnswerEvaluation } from '../types';
import '../styles/InterviewQuestion.css';

interface Props {
  sessionId: string;
  questionNumber: number;
  questionText: string;
  totalQuestions: number;
  onAnswerSubmitted: (evaluation: AnswerEvaluation) => void;
}

const InterviewQuestion: React.FC<Props> = ({
  sessionId,
  questionNumber,
  questionText,
  totalQuestions,
  onAnswerSubmitted,
}) => {
  const [phase, setPhase] = useState<'question' | 'repeat' | 'recording' | 'processing'>('question');
  const [questionSpoken, setQuestionSpoken] = useState(false);
  const [repeatCount, setRepeatCount] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(120); // 2 minutes for repeat window
  const [recordingTime, setRecordingTime] = useState(0);
  const [transcription, setTranscription] = useState('');
  const [canStopRecording, setCanStopRecording] = useState(false);
  const [error, setError] = useState('');

  const audioRecorderRef = useRef<AudioRecorder | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // Auto-speak question on mount
    speakQuestion();
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      audioRecorderRef.current?.cleanup();
    };
  }, []);

  const speakQuestion = async () => {
    try {
      const audioBlob = await apiService.textToSpeech(questionText);
      await playAudioBlob(audioBlob);
      setQuestionSpoken(true);
      setPhase('repeat');
      startRepeatTimer();
    } catch (err) {
      console.error('Error playing question:', err);
      setQuestionSpoken(true);
      setPhase('repeat');
      startRepeatTimer();
    }
  };

  const startRepeatTimer = () => {
    timerRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          if (timerRef.current) clearInterval(timerRef.current);
          startRecordingCountdown();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleRepeat = async () => {
    if (repeatCount >= 2) {
      setError('Maximum repeat limit reached');
      return;
    }

    try {
      const audioBlob = await apiService.textToSpeech(questionText);
      await playAudioBlob(audioBlob);
      setRepeatCount(repeatCount + 1);
    } catch (err) {
      setError('Failed to repeat question');
    }
  };

  const startRecordingCountdown = async () => {
    setPhase('recording');
    
    // 3-second countdown
    for (let i = 3; i > 0; i--) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    startRecording();
  };

  const startRecording = async () => {
    try {
      audioRecorderRef.current = new AudioRecorder();
      await audioRecorderRef.current.start();

      // Start recording timer
      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => {
          const newTime = prev + 1;
          
          // Enable stop button after 90 seconds
          if (newTime >= 90) {
            setCanStopRecording(true);
          }
          
          // Auto-stop at 300 seconds (5 minutes)
          if (newTime >= 300) {
            handleStopRecording();
            return 300;
          }
          
          return newTime;
        });
      }, 1000);

      // Start partial transcription every 5 seconds
      const transcriptionInterval = setInterval(async () => {
        if (audioRecorderRef.current?.isRecording()) {
          try {
            // Get partial audio recorded so far
            const partialAudio = audioRecorderRef.current.getPartialAudio();
            
            // Only transcribe if we have enough audio (at least 3 seconds worth)
            if (partialAudio.size > 10000) {
              const partialTranscription = await apiService.speechToText(partialAudio);
              setTranscription(partialTranscription);
            }
          } catch (err) {
            // Silently fail for partial transcription - we'll get full transcription at the end
            console.log('Partial transcription skipped:', err);
          }
        }
      }, 5000);

      // Store interval for cleanup
      (timerRef as any).transcriptionInterval = transcriptionInterval;
    } catch (err) {
      setError('Failed to start recording. Please check microphone permissions.');
    }
  };

  const handleStopRecording = async () => {
    if (!canStopRecording && recordingTime < 300) {
      return;
    }

    if (timerRef.current) clearInterval(timerRef.current);
    if ((timerRef as any).transcriptionInterval) {
      clearInterval((timerRef as any).transcriptionInterval);
    }

    setPhase('processing');

    try {
      const audioBlob = await audioRecorderRef.current!.stop();
      
      // Transcribe audio
      const finalTranscription = await apiService.speechToText(audioBlob);
      setTranscription(finalTranscription);

      // Submit answer
      const evaluation = await apiService.submitAnswer({
        session_id: sessionId,
        question_number: questionNumber,
        question_text: questionText,
        answer_text: finalTranscription,
      });

      onAnswerSubmitted(evaluation);
    } catch (err: any) {
      setError(err.message || 'Failed to process answer');
    }
  };

  const progress = ((questionNumber - 1) / totalQuestions) * 100;

  return (
    <div className="interview-question">
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
        <span className="progress-text">
          Question {questionNumber} of {totalQuestions}
        </span>
      </div>

      <div className="question-box">
        <h3>Question {questionNumber}</h3>
        <p>{questionText}</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {phase === 'repeat' && (
        <div className="repeat-section">
          <p className="timer">Time remaining: {formatTime(timeRemaining)}</p>
          <button
            onClick={handleRepeat}
            disabled={repeatCount >= 2}
            className="btn-secondary"
          >
            🔁 Repeat Question ({repeatCount}/2)
          </button>
          {repeatCount >= 2 && (
            <p className="info-text">Maximum repeats reached</p>
          )}
        </div>
      )}

      {phase === 'recording' && (
        <div className="recording-section">
          <div className="recording-indicator">
            <span className="recording-dot"></span>
            <span>Recording...</span>
          </div>
          <p className="recording-timer">{formatTime(recordingTime)}</p>
          <p className="recording-info">
            {canStopRecording
              ? 'You can stop recording now'
              : `Stop button available in ${formatTime(90 - recordingTime)}`}
          </p>
          
          {transcription && canStopRecording && (
            <div className="transcription-preview">
              <h4>Live Transcription Preview:</h4>
              <p>{transcription}</p>
            </div>
          )}

          {canStopRecording && (
            <button onClick={handleStopRecording} className="btn-danger">
              ⏹️ Stop & Submit
            </button>
          )}
        </div>
      )}

      {phase === 'processing' && (
        <div className="processing-section">
          <div className="spinner"></div>
          <p>Processing your answer...</p>
        </div>
      )}
    </div>
  );
};

export default InterviewQuestion;
