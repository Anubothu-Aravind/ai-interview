import io
import PyPDF2

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    return "".join(page.extract_text() or "" for page in reader.pages)
