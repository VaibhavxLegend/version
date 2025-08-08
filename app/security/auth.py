# app/security/auth.py
import jwt
import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from typing import Optional, Dict, Any
from ..config.settings import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class AuthService:
    def __init__(self):
        self.secret_key = settings.secret_key
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

auth_service = AuthService()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """Get current user from JWT token."""
    if settings.environment == "local" and settings.debug:
        # Skip authentication in local debug mode
        return {"sub": "debug_user", "role": "admin"}
    
    token = credentials.credentials
    payload = auth_service.verify_token(token)
    return payload

# Optional: API Key authentication for service-to-service calls
async def verify_api_key(api_key: str) -> bool:
    """Verify API key for service authentication."""
    if not api_key:
        return False
    
    # In production, validate against database or external service
    valid_api_keys = settings.api_keys if hasattr(settings, 'api_keys') else []
    return api_key in valid_api_keys
