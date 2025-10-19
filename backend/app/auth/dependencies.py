"""
Authentication dependencies for FastAPI endpoints.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.firebase_auth import firebase_auth
from app.database import get_db
from app.models import User
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
    Verifies Firebase token and retrieves user from database.
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        
    Returns:
        User object if authenticated
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    
    # Verify Firebase token
    decoded_token = await firebase_auth.verify_token(token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    firebase_uid = decoded_token.get("uid")
    if not firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    result = await db.execute(
        select(User).where(User.firebase_uid == firebase_uid)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in database"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_premium_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure current user has premium access.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object if has premium access
        
    Raises:
        HTTPException: If user doesn't have premium access
    """
    if not current_user.is_premium():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required for this feature"
        )
    
    return current_user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to optionally get current user.
    Returns None if no valid credentials provided.
    
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
