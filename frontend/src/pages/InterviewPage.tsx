import React, { useState } from 'react';
import InterviewSetup from '../components/InterviewSetup';
import InterviewQuestion from '../components/InterviewQuestion';
import Results from '../components/Results';
import { apiService } from '../services/api';
import { AnswerEvaluation, QAPair, InterviewResults } from '../types';
import '../styles/InterviewPage.css';

const InterviewPage: React.FC = () => {
  const [stage, setStage] = useState<'setup' | 'interview' | 'results'>('setup');
  const [sessionId, setSessionId] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [questionNumber, setQuestionNumber] = useState(1);
  const [totalQuestions] = useState(10);
  const [qaPairs, setQaPairs] = useState<QAPair[]>([]);
  const [results, setResults] = useState<InterviewResults | null>(null);

  const handleStartInterview = (newSessionId: string, firstQuestion: string) => {
    setSessionId(newSessionId);
    setCurrentQuestion(firstQuestion);
    setQuestionNumber(1);
    setStage('interview');
  };

  const handleAnswerSubmitted = async (evaluation: AnswerEvaluation) => {
    // Store the Q&A pair
    const newQA: QAPair = {
      number: questionNumber,
      question: currentQuestion,
      answer: '', // This would come from transcription
      score: evaluation.score,
      feedback: evaluation.feedback,
    };
    
    const updatedQAs = [...qaPairs, newQA];
    setQaPairs(updatedQAs);

    // Check if interview is complete
    if (questionNumber >= totalQuestions) {
      // Get final results
      const finalResults = await apiService.getResults(sessionId);
      setResults(finalResults);
      setStage('results');
    } else {
      // Get next question
      const nextQuestionNum = questionNumber + 1;
      const nextQuestion = await apiService.getNextQuestion(sessionId, nextQuestionNum);
      setCurrentQuestion(nextQuestion.question_text);
      setQuestionNumber(nextQuestionNum);
    }
  };

  const handleNewInterview = () => {
    setStage('setup');
    setSessionId('');
    setCurrentQuestion('');
    setQuestionNumber(1);
    setQaPairs([]);
    setResults(null);
  };

  return (
    <div className="interview-page">
      {stage === 'setup' && (
        <InterviewSetup onStartInterview={handleStartInterview} />
      )}

      {stage === 'interview' && (
        <InterviewQuestion
          sessionId={sessionId}
          questionNumber={questionNumber}
          questionText={currentQuestion}
          totalQuestions={totalQuestions}
          onAnswerSubmitted={handleAnswerSubmitted}
        />
      )}

      {stage === 'results' && results && (
        <Results results={results} onNewInterview={handleNewInterview} />
      )}
    </div>
  );
};

export default InterviewPage;
