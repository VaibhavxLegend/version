# app/middleware/rate_limit.py
import time
from typing import Dict, Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict, deque
import asyncio

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using sliding window algorithm."""
    
    def __init__(self, app, calls: int = 100, window: int = 60):
        super().__init__(app)
        self.calls = calls  # Number of calls allowed
        self.window = window  # Time window in seconds
        self.clients = defaultdict(deque)
        self.lock = asyncio.Lock()
    
    async def dispatch(self, request: Request, call_next):
        client_ip = self._get_client_ip(request)
        
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc"]:
            return await call_next(request)
        
        async with self.lock:
            current_time = time.time()
            
            # Clean old entries
            while (self.clients[client_ip] and 
                   self.clients[client_ip][0] < current_time - self.window):
                self.clients[client_ip].popleft()
            
            # Check if rate limit exceeded
            if len(self.clients[client_ip]) >= self.calls:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "retry_after": int(self.window - (current_time - self.clients[client_ip][0]))
                    },
                    headers={"Retry-After": str(self.window)}
                )
            
            # Add current request
            self.clients[client_ip].append(current_time)
        
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = max(0, self.calls - len(self.clients[client_ip]))
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + self.window))
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        # Check for forwarded headers (for load balancers/proxies)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"
