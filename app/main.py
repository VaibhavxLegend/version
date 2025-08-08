# app/main.py
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the deployment-ready API router (no pydantic)
try:
    from .api.endpoints_no_pydantic import router
except ImportError:
    from .api.endpoints import router

def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    - Sets metadata for interactive docs
    - Enables permissive CORS for hackathon usage
    - Mounts the HackRX API router
    - Exposes /health for uptime checks
    """
    app = FastAPI(
        title="HackRX LLM Query System",
        version="1.0.0",
        description="HackRX submission API to process PDF documents and answer questions",
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
        """Simple liveness probe to verify the service is up."""
        return {"status": "healthy", "service": "hackrx-llm-query-system"}

    # Include API router
    app.include_router(router)

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
    app,
        host="0.0.0.0",
        port=port,
    # Disable reload here to avoid duplicate imports when running as module
    reload=False
    )
