import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { Interview, QuestionDB } from '../types';
import '../styles/History.css';

const History: React.FC = () => {
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [selectedInterview, setSelectedInterview] = useState<Interview | null>(null);
  const [questions, setQuestions] = useState<QuestionDB[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadInterviews();
  }, []);

  const loadInterviews = async () => {
    setLoading(true);
    setError('');

    try {
      const data = await apiService.getAllInterviews();
      setInterviews(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load interviews');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectInterview = async (interview: Interview) => {
    setSelectedInterview(interview);
    setError('');

    try {
      const details = await apiService.getInterviewDetails(interview.id);
      setQuestions(details.questions);
    } catch (err: any) {
      setError(err.message || 'Failed to load interview details');
    }
  };

  const getScoreColor = (score: number): string => {
    if (score >= 8) return '#38ef7d';
    if (score >= 6) return '#ffd700';
    if (score >= 4) return '#ff8c00';
    return '#ff4444';
  };

  if (loading) {
    return (
      <div className="history-container">
        <div className="spinner"></div>
        <p>Loading interview history...</p>
      </div>
    );
  }

  return (
    <div className="history-container">
      <h2>📚 Interview History</h2>

      {error && <div className="error-message">{error}</div>}

      {interviews.length === 0 ? (
        <p className="no-data">No past interviews found.</p>
      ) : (
        <div className="history-layout">
          <div className="interview-list">
            <h3>Past Interviews</h3>
            {interviews.map((interview) => (
              <div
                key={interview.id}
                className={`interview-card ${selectedInterview?.id === interview.id ? 'selected' : ''}`}
                onClick={() => handleSelectInterview(interview)}
              >
                <div className="interview-header">
                  <span className="candidate-name">{interview.candidate_name}</span>
                  <span
                    className="score-badge"
                    style={{ backgroundColor: getScoreColor(interview.final_score) }}
                  >
                    {interview.final_score.toFixed(1)}/10
                  </span>
                </div>
                <p className="job-title">{interview.job_title}</p>
                <p className="interview-meta">
                  {interview.interview_type.toUpperCase()} •{' '}
                  {new Date(interview.created_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>

          <div className="interview-details">
            {selectedInterview ? (
              <>
                <h3>Interview Details</h3>
                <div className="details-info">
                  <p><strong>Candidate:</strong> {selectedInterview.candidate_name}</p>
                  <p><strong>Role:</strong> {selectedInterview.job_title}</p>
                  <p><strong>Type:</strong> {selectedInterview.interview_type.toUpperCase()}</p>
                  <p><strong>Final Score:</strong> {selectedInterview.final_score.toFixed(1)}/10</p>
                  <p>
                    <strong>Date:</strong>{' '}
                    {new Date(selectedInterview.created_at).toLocaleString()}
                  </p>
                </div>

                <h4>Questions & Answers</h4>
                <div className="questions-list">
                  {questions.map((q) => (
                    <div key={q.id} className="question-item">
                      <div className="question-header">
                        <span className="question-number">Q{q.question_number}</span>
                        <span
                          className="score-badge"
                          style={{ backgroundColor: getScoreColor(q.score) }}
                        >
                          {q.score}/10
                        </span>
                      </div>
                      <p className="question-text">
                        <strong>Question:</strong> {q.question_text}
                      </p>
                      <p className="answer-text">
                        <strong>Answer:</strong> {q.answer}
                      </p>
                      <p className="feedback-text">
                        <strong>Feedback:</strong> {q.feedback}
                      </p>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <p className="select-prompt">Select an interview to view details</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
