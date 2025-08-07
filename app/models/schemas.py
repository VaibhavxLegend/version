# app/models/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    documents: str = Field(..., description="URL to the PDF document")
    questions: List[str] = Field(..., min_items=1, max_items=20, description="List of natural language queries")

class HackathonResponse(BaseModel):
    answers: List[str] = Field(..., description="List of answers corresponding to each question")
