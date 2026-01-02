import axios from 'axios';
import {
  InterviewSetup,
  InterviewSession,
  Question,
  AnswerSubmission,
  AnswerEvaluation,
  InterviewResults,
  Interview,
  QuestionDB,
  Config,
  FileUploadResponse,
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // File upload
  uploadPDF: async (file: File): Promise<FileUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post(`${API_PREFIX}/upload/pdf`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  uploadTXT: async (file: File): Promise<FileUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post(`${API_PREFIX}/upload/txt`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // Interview management
  startInterview: async (setup: InterviewSetup): Promise<InterviewSession> => {
    const response = await api.post(`${API_PREFIX}/interview/start`, setup);
    return response.data;
  },

  getNextQuestion: async (
    sessionId: string,
    questionNumber: number
  ): Promise<Question> => {
    const response = await api.post(`${API_PREFIX}/interview/question`, {
      session_id: sessionId,
      question_number: questionNumber,
    });
    return response.data;
  },

  submitAnswer: async (
    submission: AnswerSubmission
  ): Promise<AnswerEvaluation> => {
    const response = await api.post(`${API_PREFIX}/interview/answer`, submission);
    return response.data;
  },

  getResults: async (sessionId: string): Promise<InterviewResults> => {
    const response = await api.get(`${API_PREFIX}/interview/results/${sessionId}`);
    return response.data;
  },

  saveInterview: async (sessionId: string) => {
    const response = await api.post(`${API_PREFIX}/interview/save/${sessionId}`);
    return response.data;
  },

  // Interview history
  getAllInterviews: async (): Promise<Interview[]> => {
    const response = await api.get(`${API_PREFIX}/interviews`);
    return response.data.interviews;
  },

  getInterviewDetails: async (
    interviewId: string
  ): Promise<{ interview: Interview; questions: QuestionDB[] }> => {
    const response = await api.get(`${API_PREFIX}/interviews/${interviewId}`);
    return response.data;
  },

  // Audio
  textToSpeech: async (text: string): Promise<Blob> => {
    const response = await api.post(
      `${API_PREFIX}/audio/tts`,
      { text },
      { responseType: 'blob' }
    );
    return response.data;
  },

  speechToText: async (audioBlob: Blob): Promise<string> => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.wav');
    const response = await api.post(`${API_PREFIX}/audio/stt`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data.data;
  },

  // Configuration
  getConfig: async (): Promise<Config> => {
    const response = await api.get(`${API_PREFIX}/config`);
    return response.data;
  },

  getDatabaseSchema: async (): Promise<string> => {
    const response = await api.get(`${API_PREFIX}/database/schema`);
    return response.data.schema;
  },
};
