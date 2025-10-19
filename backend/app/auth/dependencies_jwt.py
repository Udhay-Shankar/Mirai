"""
JWT Authentication dependencies for FastAPI endpoints.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.auth.jwt_handler import jwt_handler
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# HTTP Bearer token security
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user.
    Verifies JWT token and retrieves user from database.
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        
    Returns:
        User object if authenticated
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    
    # Verify JWT token
    payload = jwt_handler.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


async def get_current_premium_user(
    user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current premium user.
    Requires user to have an active premium subscription.
    
    Args:
        user: Current authenticated user
        
    Returns:
        User object if user has premium subscription
        
    Raises:
        HTTPException: If user doesn't have premium subscription
    """
    if not user.subscription_status == "premium":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required"
        )
    
    return user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Optional authentication dependency.
    Returns user if authenticated, None otherwise.
    
    Args:
        credentials: Optional HTTP Bearer token credentials
        db: Database session
        
    Returns:
        User object if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None
