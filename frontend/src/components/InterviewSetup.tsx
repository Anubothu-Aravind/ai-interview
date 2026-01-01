import React, { useState } from 'react';
import { apiService } from '../services/api';
import { InterviewSetup as InterviewSetupType } from '../types';
import '../styles/InterviewSetup.css';

interface Props {
  onStartInterview: (sessionId: string, firstQuestion: string) => void;
}

const InterviewSetup: React.FC<Props> = ({ onStartInterview }) => {
  const [candidateName, setCandidateName] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [interviewType, setInterviewType] = useState<'technical' | 'hr'>('technical');
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdFile, setJdFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!candidateName || !jobTitle || !resumeFile || !jdFile) {
      setError('Please fill all fields and upload both documents');
      return;
    }

    setLoading(true);

    try {
      // Upload resume
      const resumeResponse = resumeFile.name.endsWith('.pdf')
        ? await apiService.uploadPDF(resumeFile)
        : await apiService.uploadTXT(resumeFile);

      if (!resumeResponse.success) {
        throw new Error(resumeResponse.error || 'Failed to upload resume');
      }

      // Upload job description
      const jdResponse = jdFile.name.endsWith('.pdf')
        ? await apiService.uploadPDF(jdFile)
        : await apiService.uploadTXT(jdFile);

      if (!jdResponse.success) {
        throw new Error(jdResponse.error || 'Failed to upload job description');
      }

      // Start interview
      const setup: InterviewSetupType = {
        candidate_name: candidateName,
        job_title: jobTitle,
        interview_type: interviewType,
        resume_text: resumeResponse.text,
        jd_text: jdResponse.text,
      };

      const session = await apiService.startInterview(setup);
      onStartInterview(session.session_id, session.first_question);
    } catch (err: any) {
      setError(err.message || 'Failed to start interview');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="interview-setup">
      <h2>📋 Interview Setup</h2>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label>👤 Candidate Name</label>
            <input
              type="text"
              value={candidateName}
              onChange={(e) => setCandidateName(e.target.value)}
              placeholder="John Doe"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label>💼 Job Title</label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              placeholder="Software Engineer"
              disabled={loading}
            />
          </div>
        </div>

        <div className="form-group">
          <label>📝 Interview Type</label>
          <select
            value={interviewType}
            onChange={(e) => setInterviewType(e.target.value as 'technical' | 'hr')}
            disabled={loading}
          >
            <option value="technical">Technical</option>
            <option value="hr">HR</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>📄 Resume (PDF or TXT)</label>
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
              disabled={loading}
            />
            {resumeFile && <span className="file-name">{resumeFile.name}</span>}
          </div>

          <div className="form-group">
            <label>📄 Job Description (PDF or TXT)</label>
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={(e) => setJdFile(e.target.files?.[0] || null)}
              disabled={loading}
            />
            {jdFile && <span className="file-name">{jdFile.name}</span>}
          </div>
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? '🔄 Starting Interview...' : '🚀 Start Interview'}
        </button>
      </form>
    </div>
  );
};

export default InterviewSetup;
