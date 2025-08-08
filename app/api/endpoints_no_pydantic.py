# app/api/endpoints_no_pydantic.py
# Emergency deployment version without Pydantic to avoid Rust compilation

import asyncio
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
from ..services.pdf_processing import SimplePDFProcessor
from ..services.llm import GeminiLLM, force_single_line
import requests
import concurrent.futures

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
        
        # Limit number of questions to prevent worker timeout
        limited_questions = validated_data["questions"][:10]  # Max 10 questions
        limited_text = extracted_text[:3000]  # Max 3000 chars

        def sync_llm_answer(question):
            try:
                if extracted_text and "Unable to extract" not in extracted_text and "Error:" not in extracted_text:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        answer = loop.run_until_complete(
                            asyncio.wait_for(
                                llm_service.generate_single_line_answer(question, [limited_text]),
                                timeout=5.0
                            )
                        )
                    except asyncio.TimeoutError:
                        answer = "Processing timeout - unable to analyze this question."
                    finally:
                        loop.close()
                else:
                    answer = "Unable to process the document content to answer this question."
            except Exception:
                answer = "Processing error occurred for this question."
            answer = force_single_line(answer)
            if len(answer) > 200:
                answer = answer[:197] + "..."
            return answer

        answers = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(sync_llm_answer, q) for q in limited_questions]
            # Collect results in the original order
            for future in futures:
                answers.append(future.result())

        # Final sanitization: remove actual and literal "\n" from each answer
        cleaned_answers = []
        for a in answers:
            if not isinstance(a, str):
                a = str(a)
            # Replace literal backslash-n and real newlines/carriage returns
            a = a.replace("\\n", " ").replace("\n", " ").replace("\r", " ")
            # Collapse excess whitespace
            a = " ".join(a.split())
            cleaned_answers.append(a)

        # Return response in correct format
        return create_hackathon_response(cleaned_answers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
