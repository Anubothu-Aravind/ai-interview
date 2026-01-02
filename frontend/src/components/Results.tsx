import React, { useState } from 'react';
import { InterviewResults as InterviewResultsType } from '../types';
import { apiService } from '../services/api';
import '../styles/Results.css';

interface Props {
  results: InterviewResultsType;
  onNewInterview: () => void;
}

const Results: React.FC<Props> = ({ results, onNewInterview }) => {
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');

  const handleSave = async () => {
    setSaving(true);
    setError('');

    try {
      await apiService.saveInterview(results.session_id);
      setSaved(true);
    } catch (err: any) {
      setError(err.message || 'Failed to save interview');
    } finally {
      setSaving(false);
    }
  };

  const getScoreColor = (score: number): string => {
    if (score >= 8) return '#38ef7d';
    if (score >= 6) return '#ffd700';
    if (score >= 4) return '#ff8c00';
    return '#ff4444';
  };

  return (
    <div className="results-container">
      <h2>🎉 Interview Completed!</h2>

      <div className="score-card" style={{ background: `linear-gradient(135deg, #11998e 0%, ${getScoreColor(results.final_score)} 100%)` }}>
        <div className="final-score">{results.final_score.toFixed(1)}/10</div>
        <div className="score-label">Overall Score</div>
        <div className="percentage">{results.percentage.toFixed(0)}%</div>
      </div>

      <div className="interview-info">
        <p><strong>Candidate:</strong> {results.candidate_name}</p>
        <p><strong>Position:</strong> {results.job_title}</p>
        <p><strong>Interview Type:</strong> {results.interview_type.toUpperCase()}</p>
        <p><strong>Date:</strong> {new Date(results.completed_at).toLocaleDateString()}</p>
      </div>

      <h3>📊 Detailed Results</h3>

      <div className="qa-list">
        {results.qa_pairs.map((qa) => (
          <div key={qa.number} className="qa-item">
            <div className="qa-header">
              <span className="question-number">Q{qa.number}</span>
              <span className="score-badge" style={{ backgroundColor: getScoreColor(qa.score) }}>
                {qa.score}/10
              </span>
            </div>
            <div className="qa-content">
              <p className="question"><strong>Question:</strong> {qa.question}</p>
              <p className="answer"><strong>Answer:</strong> {qa.answer}</p>
              <p className="feedback"><strong>Feedback:</strong> {qa.feedback}</p>
            </div>
          </div>
        ))}
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="actions">
        {!saved && (
          <button onClick={handleSave} disabled={saving} className="btn-primary">
            {saving ? '💾 Saving...' : '💾 Save to Database'}
          </button>
        )}
        {saved && <p className="success-message">✅ Interview saved successfully!</p>}
        
        <button onClick={onNewInterview} className="btn-secondary">
          🔄 Start New Interview
        </button>
      </div>
    </div>
  );
};

export default Results;
