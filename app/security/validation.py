# app/security/validation.py
import base64
import re
from typing import Optional, List
from fastapi import HTTPException
from pydantic import validator, ValidationError

class SecurityValidator:
    """Security validation utilities."""
    
    @staticmethod
    def validate_base64_pdf(pdf_blob: str, max_size_mb: int = 50) -> bool:
        """
        Validate base64 PDF blob.
        
        Args:
            pdf_blob: Base64 encoded PDF string
            max_size_mb: Maximum allowed file size in MB
            
        Returns:
            bool: True if valid
            
        Raises:
            HTTPException: If validation fails
        """
        if not pdf_blob:
            raise HTTPException(status_code=400, detail="PDF blob cannot be empty")
        
        try:
            # Decode base64 to check validity
            pdf_bytes = base64.b64decode(pdf_blob)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid base64 encoding")
        
        # Check file size
        size_mb = len(pdf_bytes) / (1024 * 1024)
        if size_mb > max_size_mb:
            raise HTTPException(
                status_code=413,
                detail=f"PDF file too large. Maximum size: {max_size_mb}MB, received: {size_mb:.2f}MB"
            )
        
        # Check PDF magic bytes
        if not pdf_bytes.startswith(b'%PDF'):
            raise HTTPException(status_code=400, detail="File is not a valid PDF")
        
        return True
    
    @staticmethod
    def validate_questions(questions: List[str], max_questions: int = 10, max_length: int = 1000) -> bool:
        """
        Validate question list.
        
        Args:
            questions: List of question strings
            max_questions: Maximum number of questions allowed
            max_length: Maximum length per question
            
        Returns:
            bool: True if valid
            
        Raises:
            HTTPException: If validation fails
        """
        if not questions:
            raise HTTPException(status_code=400, detail="At least one question is required")
        
        if len(questions) > max_questions:
            raise HTTPException(
                status_code=400,
                detail=f"Too many questions. Maximum: {max_questions}, received: {len(questions)}"
            )
        
        for i, question in enumerate(questions):
            if not question or not question.strip():
                raise HTTPException(status_code=400, detail=f"Question {i+1} cannot be empty")
            
            if len(question) > max_length:
                raise HTTPException(
                    status_code=400,
                    detail=f"Question {i+1} too long. Maximum: {max_length} characters"
                )
            
            # Check for potential injection attempts
            if SecurityValidator._contains_suspicious_patterns(question):
                raise HTTPException(
                    status_code=400,
                    detail=f"Question {i+1} contains suspicious content"
                )
        
        return True
    
    @staticmethod
    def _contains_suspicious_patterns(text: str) -> bool:
        """Check for suspicious patterns that might indicate injection attempts."""
        suspicious_patterns = [
            r'<script.*?>',
            r'javascript:',
            r'onload=',
            r'onerror=',
            r'eval\s*\(',
            r'exec\s*\(',
            r'\.\./',
            r'\\.\\.\\',
            r'union\s+select',
            r'drop\s+table',
            r'delete\s+from',
            r'insert\s+into',
            r'update\s+.*\s+set',
        ]
        
        text_lower = text.lower()
        for pattern in suspicious_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        if not filename:
            return "unnamed_file"
        
        # Remove directory traversal attempts
        filename = re.sub(r'[/\\]', '_', filename)
        filename = re.sub(r'\.\.', '_', filename)
        
        # Remove special characters
        filename = re.sub(r'[<>:"|?*]', '_', filename)
        
        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:250] + ('.' + ext if ext else '')
        
        return filename or "unnamed_file"

# Pydantic validators for request models
def validate_pdf_size(v: str) -> str:
    """Pydantic validator for PDF size."""
    SecurityValidator.validate_base64_pdf(v)
    return v

def validate_question_list(v: List[str]) -> List[str]:
    """Pydantic validator for questions."""
    SecurityValidator.validate_questions(v)
    return v
