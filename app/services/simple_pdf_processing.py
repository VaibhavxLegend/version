# app/services/simple_pdf_processing.py
import base64
import io
from typing import Optional
from PyPDF2 import PdfReader

class SimplePDFProcessor:
    def __init__(self):
        pass

    async def base64_to_markdown(self, pdf_blob_base64: str) -> Optional[str]:
        """
        Convert base64 PDF blob to plain text using PyPDF2.
        """
        try:
            pdf_bytes = base64.b64decode(pdf_blob_base64)
            raw_text = self._extract_text_from_pdf(pdf_bytes)
            return raw_text
        except Exception as e:
            print(f"Failed to convert PDF blob to text: {e}")
            return None

    def _extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """
        Extract text from PDF bytes using PyPDF2.
        """
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_file)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text if text.strip() else "No text could be extracted from the PDF."
            
        except Exception as e:
            print(f"Failed to extract text from PDF: {e}")
            return "Error: Could not process the PDF document."
