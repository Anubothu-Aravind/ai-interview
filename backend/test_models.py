import pytest
from backend.models import (
    InterviewSetup,
    Question,
    AnswerSubmission,
    AnswerEvaluation,
    QAPair,
)


def test_interview_setup_validation():
    """Test InterviewSetup model validation"""
    setup = InterviewSetup(
        candidate_name="John Doe",
        job_title="Software Engineer",
        interview_type="technical",
        resume_text="Sample resume text",
        jd_text="Sample job description",
    )
    assert setup.candidate_name == "John Doe"
    assert setup.interview_type in ["technical", "hr"]


def test_question_model():
    """Test Question model"""
    question = Question(question_number=1, question_text="Tell me about yourself")
    assert question.question_number == 1
    assert len(question.question_text) > 0


def test_answer_submission_model():
    """Test AnswerSubmission model"""
    submission = AnswerSubmission(
        session_id="test-session-123",
        question_number=1,
        question_text="What is your experience?",
        answer_text="I have 5 years of experience",
    )
    assert submission.session_id == "test-session-123"
    assert submission.question_number == 1


def test_answer_evaluation_model():
    """Test AnswerEvaluation model"""
    evaluation = AnswerEvaluation(
        score=8.5, feedback="Good answer with relevant details"
    )
    assert 0 <= evaluation.score <= 10
    assert len(evaluation.feedback) > 0


def test_qa_pair_model():
    """Test QAPair model"""
    qa_pair = QAPair(
        number=1,
        question="What is your background?",
        answer="I have a CS degree",
        score=7.0,
        feedback="Could provide more details",
    )
    assert qa_pair.number == 1
    assert qa_pair.score >= 0
