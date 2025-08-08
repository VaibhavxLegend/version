# app/api/endpoints_no_pydantic.py
# Emergency deployment version without Pydantic to avoid Rust compilation

import base64
import re
import json
from fastapi import APIRouter, HTTPException, Header, Request
from typing import List, Dict, Any, Optional
from ..models.manual_schemas import (
    validate_query_request, 
    create_hackathon_response,
    ValidationError
)
from ..services.simple_pdf_processing import SimplePDFProcessor
from ..services.llm import GeminiLLM
import requests

# Expected bearer token for the hackathon
HACKATHON_TOKEN = "cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a"

router = APIRouter(prefix="/hackrx", tags=["HackRX"])
pdf_processor = SimplePDFProcessor()
llm_service = GeminiLLM()

def verify_token(authorization: Optional[str] = Header(None)):
    """Verify the bearer token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.split(" ")[1]
    if token != HACKATHON_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token

@router.post("/run")
async def run_submission(
    request: Request,
    authorization: Optional[str] = Header(None, description="Bearer token for authentication")
):
    """
    Process document from URL and answer queries for HackRX competition.
    """
    # Verify authentication
    verify_token(authorization)
    
    try:
        # Get JSON data manually
        raw_data = await request.json()
        
        # Validate request data manually
        try:
            validated_data = validate_query_request(raw_data)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=str(e))
        
        # Download the PDF from the provided URL
        response = requests.get(validated_data["documents"], timeout=30)
        response.raise_for_status()
        
        # Process the PDF content
        pdf_content = response.content
        
        # Convert PDF to base64 for processing
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
        
        # Extract text from PDF
        extracted_text = await pdf_processor.base64_to_markdown(pdf_base64)
        
        if not extracted_text or extracted_text.strip() == "":
            extracted_text = "Unable to extract text from the provided PDF document."
        
        # Process each question against the extracted text
        answers = []
        
        for question in validated_data["questions"]:
            if extracted_text and "Unable to extract" not in extracted_text and "Error:" not in extracted_text:
                # Use LLM service to generate single-line answer
                answer = await llm_service.generate_single_line_answer(question, [extracted_text])
            else:
                # Fallback to indicating document processing issues
                answer = "Unable to process the document content to answer this question."
            
            answers.append(answer)
        
        # Return response in correct format
        return create_hackathon_response(answers)
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to download document: {str(e)}"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail="Invalid JSON in request body"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

@router.get("/health")
async def hackrx_health_check():
    """Health check for HackRX submission."""
    return {
        "status": "healthy",
        "service": "hackrx-submission",
        "endpoint": "/hackrx/run",
        "version": "no-pydantic"
    }
