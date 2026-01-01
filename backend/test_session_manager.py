import pytest
from backend.session_manager import session_manager, SessionManager
from backend.models import QAPair


def test_create_session():
    """Test creating a new interview session"""
    manager = SessionManager()
    
    session_id = manager.create_session(
        candidate_name="Test User",
        job_title="Developer",
        interview_type="technical",
        resume="Test resume",
        jd="Test JD",
    )
    
    assert session_id is not None
    assert len(session_id) > 0
    assert session_id in manager.sessions


def test_get_session():
    """Test retrieving a session"""
    manager = SessionManager()
    
    session_id = manager.create_session(
        candidate_name="Test User",
        job_title="Developer",
        interview_type="technical",
        resume="Test resume",
        jd="Test JD",
    )
    
    session = manager.get_session(session_id)
    assert session is not None
    assert session.candidate_name == "Test User"
    assert session.total_questions == 10


def test_add_conversation():
    """Test adding conversation history"""
    manager = SessionManager()
    
    session_id = manager.create_session(
        candidate_name="Test User",
        job_title="Developer",
        interview_type="technical",
        resume="Test resume",
        jd="Test JD",
    )
    
    manager.add_conversation(session_id, "Question 1", "Answer 1")
    history = manager.get_conversation_history(session_id)
    
    assert len(history) == 1
    assert history[0]["question"] == "Question 1"
    assert history[0]["answer"] == "Answer 1"


def test_add_qa_pair():
    """Test adding Q&A pairs"""
    manager = SessionManager()
    
    session_id = manager.create_session(
        candidate_name="Test User",
        job_title="Developer",
        interview_type="technical",
        resume="Test resume",
        jd="Test JD",
    )
    
    qa_pair = QAPair(
        number=1,
        question="Test question",
        answer="Test answer",
        score=8.0,
        feedback="Good",
    )
    
    manager.add_qa_pair(session_id, qa_pair)
    qa_pairs = manager.get_qa_pairs(session_id)
    
    assert len(qa_pairs) == 1
    assert qa_pairs[0].score == 8.0


def test_delete_session():
    """Test deleting a session"""
    manager = SessionManager()
    
    session_id = manager.create_session(
        candidate_name="Test User",
        job_title="Developer",
        interview_type="technical",
        resume="Test resume",
        jd="Test JD",
    )
    
    manager.delete_session(session_id)
    
    assert session_id not in manager.sessions
    assert session_id not in manager.conversation_history
    assert session_id not in manager.qa_pairs
