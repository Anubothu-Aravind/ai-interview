import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_get_config():
    """Test configuration endpoint"""
    response = client.get("/api/v1/config")
    assert response.status_code == 200
    data = response.json()
    assert "total_questions" in data
    assert "repeat_window_seconds" in data
    assert "record_max_time_seconds" in data


def test_get_database_schema():
    """Test database schema endpoint"""
    response = client.get("/api/v1/database/schema")
    assert response.status_code == 200
    data = response.json()
    assert "schema" in data
    assert "CREATE TABLE" in data["schema"]


def test_upload_txt_invalid_file():
    """Test uploading invalid file type"""
    files = {"file": ("test.doc", b"test content", "application/msword")}
    response = client.post("/api/v1/upload/txt", files=files)
    # Should return 400 for invalid file type
    assert response.status_code == 400
