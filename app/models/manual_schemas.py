# app/models/manual_schemas.py
# Manual validation schemas without Pydantic to avoid Rust compilation

from typing import List, Dict, Any, Optional
import json

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_query_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Manually validate request data"""
    if not isinstance(data, dict):
        raise ValidationError("Request must be a JSON object")
    
    # Check required fields
    if "documents" not in data:
        raise ValidationError("Field 'documents' is required")
    
    if not isinstance(data["documents"], str):
        raise ValidationError("Field 'documents' must be a string URL")
    
    # Questions field is optional, default to empty list
    questions = data.get("questions", [])
    if not isinstance(questions, list):
        raise ValidationError("Field 'questions' must be a list")
    
    # Validate each question is a string
    for i, question in enumerate(questions):
        if not isinstance(question, str):
            raise ValidationError(f"Question {i} must be a string")
    
    return {
        "documents": data["documents"],
        "questions": questions
    }

def create_hackathon_response(answers: List[str]) -> Dict[str, Any]:
    """Create response in HackathonResponse format"""
    return {"answers": answers}

class QueryRequest:
    """Simple class to hold validated request data"""
    def __init__(self, documents: str, questions: List[str] = None):
        self.documents = documents
        self.questions = questions or []

class HackathonResponse:
    """Simple class to hold response data"""
    def __init__(self, answers: List[str]):
        self.answers = answers
    
    def dict(self):
        return {"answers": self.answers}
