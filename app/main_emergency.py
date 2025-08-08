# app/main_emergency.py
# Emergency deployment version without Pydantic to avoid Rust compilation

import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the no-pydantic API router
from .api.endpoints_no_pydantic import router

def create_app() -> FastAPI:
    app = FastAPI(
        title="HackRX LLM Query System",
        version="1.0.0",
        description="HackRX submission API to process PDF documents and answer questions (No Pydantic)",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Add CORS middleware - allow all origins for hackathon
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy", 
            "service": "hackrx-llm-query-system",
            "version": "emergency-no-pydantic"
        }

    # Include API router
    app.include_router(router)

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main_emergency:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload for production
    )
