import io
import PyPDF2

def extract_text_from_pdf(file):
    """
    Extracts and concatenates text from all pages of a PDF provided via a readable file-like object.
    
    Parameters:
        file (io.BufferedReader or file-like): A readable binary stream or file-like object containing PDF data; the function will read the stream fully.
    
    Returns:
        str: The concatenated text from every page of the PDF (pages with no extractable text contribute an empty string).
    """
    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    return "".join(page.extract_text() or "" for page in reader.pages)