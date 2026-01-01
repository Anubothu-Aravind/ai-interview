import pytest
from backend.utils import (
    extract_text_from_pdf,
    extract_text_from_txt,
    validate_file_extension,
)


def test_extract_text_from_txt():
    """Test text extraction from TXT content"""
    test_content = b"This is a test document"
    result = extract_text_from_txt(test_content)
    assert result == "This is a test document"


def test_validate_file_extension_valid():
    """Test file extension validation with valid extensions"""
    assert validate_file_extension("document.pdf", [".pdf", ".txt"]) is True
    assert validate_file_extension("file.txt", [".pdf", ".txt"]) is True
    assert validate_file_extension("RESUME.PDF", [".pdf", ".txt"]) is True


def test_validate_file_extension_invalid():
    """Test file extension validation with invalid extensions"""
    assert validate_file_extension("document.doc", [".pdf", ".txt"]) is False
    assert validate_file_extension("file.docx", [".pdf", ".txt"]) is False
    assert validate_file_extension("image.jpg", [".pdf", ".txt"]) is False


def test_validate_file_extension_case_insensitive():
    """Test that validation is case insensitive"""
    assert validate_file_extension("file.PDF", [".pdf"]) is True
    assert validate_file_extension("file.TXT", [".txt"]) is True
