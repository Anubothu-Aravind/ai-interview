import io
import PyPDF2
from typing import Optional

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract text from PDF file bytes"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

def extract_text_from_txt(txt_content: bytes) -> str:
    """Extract text from TXT file bytes"""
    try:
        return txt_content.decode('utf-8')
    except Exception as e:
        print(f"Error extracting TXT text: {e}")
        return ""

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate file extension"""
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)
