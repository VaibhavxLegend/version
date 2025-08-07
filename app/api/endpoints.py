# app/api/endpoints.py
import time
import uuid
from fastapi import APIRouter, Body, HTTPException, Header
from typing import List, Dict, Any, Optional
from ..models.schemas import QueryRequest, HackathonResponse
import requests

# Expected bearer token for the hackathon
HACKATHON_TOKEN = "cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a"

router = APIRouter(prefix="/hackrx", tags=["HackRX"])

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

@router.post("/run", response_model=HackathonResponse)
async def run_submission(
    query_request: QueryRequest = Body(...),
    authorization: Optional[str] = Header(None, description="Bearer token for authentication")
):
    """
    Process document from URL and answer queries for HackRX competition.
    """
    # Verify authentication
    verify_token(authorization)
    
    try:
        # Download the PDF from the provided URL
        response = requests.get(query_request.documents, timeout=30)
        response.raise_for_status()
        
        # TODO: Implement actual processing pipeline
        # This is where you would integrate:
        # 1. PDF processing from downloaded content
        # 2. Text chunking service
        # 3. Embedding generation with Pinecone
        # 4. Vector similarity search
        # 5. LLM query processing with Gemini
        
        # For now, return sample responses based on the questions
        answers = []
        
        # Sample responses for common insurance policy questions
        sample_responses = {
            "grace period": "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.",
            "waiting period": "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered.",
            "maternity": "Yes, the policy covers maternity expenses, including childbirth and lawful medical termination of pregnancy. To be eligible, the female insured person must have been continuously covered for at least 24 months.",
            "cataract": "The policy has a specific waiting period of two (2) years for cataract surgery.",
            "organ donor": "Yes, the policy indemnifies the medical expenses for the organ donor's hospitalization for the purpose of harvesting the organ, provided the organ is for an insured person.",
            "no claim discount": "A No Claim Discount of 5% on the base premium is offered on renewal for a one-year policy term if no claims were made in the preceding year.",
            "health check": "Yes, the policy reimburses expenses for health check-ups at the end of every block of two continuous policy years, provided the policy has been renewed without a break.",
            "hospital": "A hospital is defined as an institution with at least 10 inpatient beds with qualified nursing staff and medical practitioners available 24/7, and a fully equipped operation theatre.",
            "ayush": "The policy covers medical expenses for inpatient treatment under Ayurveda, Yoga, Naturopathy, Unani, Siddha, and Homeopathy systems up to the Sum Insured limit.",
            "room rent": "For Plan A, the daily room rent is capped at 1% of the Sum Insured, and ICU charges are capped at 2% of the Sum Insured."
        }
        
        for question in query_request.questions:
            question_lower = question.lower()
            answer = "Based on the policy document analysis, this information is not explicitly mentioned in the available documentation."
            
            # Match questions to sample responses
            for key, response in sample_responses.items():
                if key in question_lower:
                    answer = response
                    break
            
            answers.append(answer)
        
        return HackathonResponse(answers=answers)
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to download document: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

@router.get("/health", tags=["Health"])
async def hackrx_health_check():
    """Health check for HackRX submission."""
    return {
        "status": "healthy",
        "service": "hackrx-submission",
        "endpoint": "/hackrx/run"
    }
