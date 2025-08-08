# app/middleware/security.py
import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from ..utils.logging import get_logger

logger = get_logger(__name__)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID for tracking
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.time()
        
        # Log incoming request
        logger.info(
            f"Request {request_id}: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        response = await call_next(request)
        
        # Add security headers
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; "
                "connect-src 'self'"
            ),
            "X-Request-ID": request_id,
            "X-Response-Time": f"{(time.time() - start_time) * 1000:.2f}ms"
        }
        
        for header, value in security_headers.items():
            response.headers[header] = value
        
        # Remove server information
        if "server" in response.headers:
            del response.headers["server"]
        
        # Log response
        logger.info(
            f"Response {request_id}: {response.status_code} "
            f"({(time.time() - start_time) * 1000:.2f}ms)"
        )
        
        return response

class CORSSecurityMiddleware(BaseHTTPMiddleware):
    """Enhanced CORS middleware with security considerations."""
    
    def __init__(self, app, allowed_origins: list = None, environment: str = "production"):
        super().__init__(app)
        self.environment = environment
        
        # Set allowed origins based on environment
        if environment == "local" or environment == "development":
            self.allowed_origins = ["http://localhost:*", "http://127.0.0.1:*"] if not allowed_origins else allowed_origins
        else:
            # Production should have explicit allowed origins
            self.allowed_origins = allowed_origins or []
    
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        
        # Handle preflight requests
        if request.method == "OPTIONS":
            if self._is_allowed_origin(origin):
                response = Response()
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Max-Age"] = "600"
                return response
            else:
                return Response(status_code=403, content="CORS: Origin not allowed")
        
        response = await call_next(request)
        
        # Add CORS headers for allowed origins
        if self._is_allowed_origin(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response
    
    def _is_allowed_origin(self, origin: str) -> bool:
        """Check if origin is allowed."""
        if not origin:
            return False
        
        # In development, allow localhost variations
        if self.environment in ["local", "development"]:
            if origin.startswith("http://localhost") or origin.startswith("http://127.0.0.1"):
                return True
        
        return origin in self.allowed_origins
