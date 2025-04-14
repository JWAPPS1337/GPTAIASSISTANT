import os
import jwt
from fastapi import Request, HTTPException
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Middleware to verify JWT tokens
# This doesn't enforce authentication but validates tokens if present
class JWTMiddleware:
    async def __call__(self, request: Request, call_next):
        # Get JWT secret from environment variable
        jwt_secret = os.environ.get("JWT_SECRET")
        
        # If no JWT_SECRET is set, skip token validation
        if not jwt_secret:
            logger.warning("JWT_SECRET is not set. Authentication is disabled.")
            return await call_next(request)
        
        # Extract token from Authorization header
        authorization = request.headers.get("Authorization")
        token = None
        
        if authorization and authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
        
        # Add token info to request state for endpoint handlers to access
        request.state.token = token
        request.state.user = None
        
        # If token is present, try to validate it
        if token:
            try:
                # Decode and verify token
                payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
                # Add user info to request state
                request.state.user = {
                    "id": payload.get("sub"),
                    "email": payload.get("email"),
                    "name": payload.get("name")
                }
                logger.debug(f"Authenticated user: {request.state.user['email']}")
            except jwt.ExpiredSignatureError:
                logger.warning("Token expired")
                # Continue processing the request but with no valid user
            except jwt.InvalidTokenError as e:
                logger.warning(f"Invalid token: {str(e)}")
                # Continue processing the request but with no valid user
        
        # Proceed with the request
        return await call_next(request)

# Optional dependency for endpoints that require authentication
def get_current_user(request: Request) -> Optional[dict]:
    user = request.state.user
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )
    return user 