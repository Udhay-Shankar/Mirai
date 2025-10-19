"""
Authentication router for user registration and login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import logging

from app.database import get_db
from app.models import User, SubscriptionTier
from app.auth.firebase_auth import firebase_auth
from app.auth.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    """User registration request."""
    firebase_token: str
    provider: str  # google, facebook, email, phone


class UserResponse(BaseModel):
    """User response model."""
    id: int
    email: Optional[str]
    phone_number: Optional[str]
    display_name: Optional[str]
    photo_url: Optional[str]
    provider: str
    subscription_tier: SubscriptionTier
    is_premium: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user after Firebase authentication.
    
    Args:
        request: Registration request with Firebase token
        db: Database session
        
    Returns:
        Created user information
    """
    # Verify Firebase token
    decoded_token = await firebase_auth.verify_token(request.firebase_token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )
    
    firebase_uid = decoded_token.get("uid")
    email = decoded_token.get("email")
    phone = decoded_token.get("phone_number")
    name = decoded_token.get("name")
    picture = decoded_token.get("picture")
    
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.firebase_uid == firebase_uid)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        # Update last login
        existing_user.last_login = datetime.now()
        await db.commit()
        await db.refresh(existing_user)
        
        return UserResponse(
            id=existing_user.id,
            email=existing_user.email,
            phone_number=existing_user.phone_number,
            display_name=existing_user.display_name,
            photo_url=existing_user.photo_url,
            provider=existing_user.provider,
            subscription_tier=existing_user.subscription_tier,
            is_premium=existing_user.is_premium(),
            created_at=existing_user.created_at
        )
    
    # Create new user
    new_user = User(
        firebase_uid=firebase_uid,
        email=email,
        phone_number=phone,
        display_name=name,
        photo_url=picture,
        provider=request.provider,
        subscription_tier=SubscriptionTier.FREE,
        last_login=datetime.now()
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    logger.info(f"New user registered: {new_user.id} ({email or phone})")
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        phone_number=new_user.phone_number,
        display_name=new_user.display_name,
        photo_url=new_user.photo_url,
        provider=new_user.provider,
        subscription_tier=new_user.subscription_tier,
        is_premium=new_user.is_premium(),
        created_at=new_user.created_at
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        User information
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        phone_number=current_user.phone_number,
        display_name=current_user.display_name,
        photo_url=current_user.photo_url,
        provider=current_user.provider,
        subscription_tier=current_user.subscription_tier,
        is_premium=current_user.is_premium(),
        created_at=current_user.created_at
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user.
    Revokes Firebase refresh tokens.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Success message
    """
    # Revoke Firebase tokens
    await firebase_auth.revoke_refresh_tokens(current_user.firebase_uid)
    
    logger.info(f"User logged out: {current_user.id}")
    
    return {"message": "Successfully logged out"}


@router.post("/verify-token")
async def verify_token(request: RegisterRequest):
    """
    Verify Firebase token without registration.
    
    Args:
        request: Token verification request
        
    Returns:
        Token validity status
    """
    decoded_token = await firebase_auth.verify_token(request.firebase_token)
    
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return {
        "valid": True,
        "uid": decoded_token.get("uid"),
        "email": decoded_token.get("email"),
        "phone": decoded_token.get("phone_number")
    }
