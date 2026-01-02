export interface InterviewSetup {
  candidate_name: string;
  job_title: string;
  interview_type: 'technical' | 'hr';
  resume_text: string;
  jd_text: string;
}

export interface InterviewSession {
  session_id: string;
  first_question: string;
  total_questions: number;
}

export interface Question {
  question_number: number;
  question_text: string;
}

export interface AnswerSubmission {
  session_id: string;
  question_number: number;
  question_text: string;
  answer_text: string;
}

export interface AnswerEvaluation {
  score: number;
  feedback: string;
}

export interface QAPair {
  number: number;
  question: string;
  answer: string;
  score: number;
  feedback: string;
}

export interface InterviewResults {
  session_id: string;
  candidate_name: string;
  job_title: string;
  interview_type: string;
  final_score: number;
  percentage: number;
  qa_pairs: QAPair[];
  start_time: string;
  completed_at: string;
}

export interface Interview {
  id: string;
  candidate_name: string;
  job_title: string;
  interview_type: string;
  final_score: number;
  start_time: string;
  completed_at: string;
  created_at: string;
}

export interface QuestionDB {
  id: string;
  interview_id: string;
  question_number: number;
  question_text: string;
  answer: string;
  score: number;
  feedback: string;
  created_at: string;
}

export interface Config {
  total_questions: number;
  repeat_window_seconds: number;
  record_max_time_seconds: number;
  stop_button_time_seconds: number;
  preview_time_seconds: number;
}

export interface FileUploadResponse {
  success: boolean;
  text: string;
  error?: string;
}
