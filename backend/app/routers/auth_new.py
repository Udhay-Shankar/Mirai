"""
Authentication router with JWT and OAuth support.
Supports: Email/Password, Google, Facebook, Twitter/X, Instagram
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import logging
import os

from app.database import get_db
from app.models import User, SubscriptionTier
from app.auth.jwt_handler import jwt_handler
from app.auth.oauth_providers import oauth
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Frontend URL for OAuth redirects
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')


# Request/Response Models
class UserRegister(BaseModel):
    """Email/password registration request."""
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """Email/password login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class UserResponse(BaseModel):
    """User response model."""
    id: int
    email: Optional[str]
    full_name: Optional[str]
    photo_url: Optional[str]
    provider: str
    subscription_tier: SubscriptionTier
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


# Helper function to get current user from JWT
async def get_current_user_from_token(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    """Extract and verify JWT token from request."""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = auth_header.split(' ')[1]
    payload = jwt_handler.decode_token(token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return user


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user with email and password.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Access and refresh tokens with user data
    """
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = jwt_handler.hash_password(user_data.password)
    
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        provider="email",
        subscription_tier=SubscriptionTier.FREE,
        is_active=True,
        created_at=datetime.utcnow(),
        last_login=datetime.utcnow()
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Generate tokens
    access_token = jwt_handler.create_access_token(data={"sub": str(new_user.id)})
    refresh_token = jwt_handler.create_refresh_token(data={"sub": str(new_user.id)})
    
    logger.info(f"New user registered: {new_user.email}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "provider": new_user.provider,
            "subscription_tier": new_user.subscription_tier.value
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.
    
    Args:
        credentials: User login credentials
        db: Database session
        
    Returns:
        Access and refresh tokens with user data
    """
    # Find user
    result = await db.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not jwt_handler.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    # Generate tokens
    access_token = jwt_handler.create_access_token(data={"sub": str(user.id)})
    refresh_token = jwt_handler.create_refresh_token(data={"sub": str(user.id)})
    
    logger.info(f"User logged in: {user.email}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "provider": user.provider,
            "subscription_tier": user.subscription_tier.value
        }
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Args:
        token_data: Refresh token
        db: Database session
        
    Returns:
        New access and refresh tokens
    """
    payload = jwt_handler.decode_token(token_data.refresh_token)
    
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Generate new tokens
    access_token = jwt_handler.create_access_token(data={"sub": str(user.id)})
    refresh_token = jwt_handler.create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "provider": user.provider,
            "subscription_tier": user.subscription_tier.value
        }
    )


# OAuth Routes

@router.get("/oauth/{provider}")
async def oauth_login(provider: str, request: Request):
    """
    Initiate OAuth login flow.
    Supports: google, facebook, twitter, instagram
    
    Args:
        provider: OAuth provider name
        request: FastAPI request object
        
    Returns:
        Redirect to OAuth provider
    """
    if provider not in ['google', 'facebook', 'twitter', 'instagram']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {provider}"
        )
    
    # Check if OAuth provider is configured
    client_id = None
    if provider == 'google':
        client_id = settings.google_client_id
    elif provider == 'facebook':
        client_id = settings.facebook_client_id
    elif provider == 'twitter':
        client_id = settings.twitter_client_id
    elif provider == 'instagram':
        client_id = settings.instagram_client_id
    
    if not client_id or client_id.startswith('your_'):
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"{provider.capitalize()} OAuth is not configured yet. Please use email/password login or contact the administrator to set up {provider.capitalize()} authentication."
        )
    
    try:
        redirect_uri = str(request.url_for('oauth_callback', provider=provider))
        return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)
    except Exception as e:
        logger.error(f"OAuth {provider} error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize {provider.capitalize()} OAuth. Please try email/password login instead."
        )


@router.get("/oauth/{provider}/callback")
async def oauth_callback(
    provider: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Handle OAuth callback and create/login user.
    
    Args:
        provider: OAuth provider name
        request: FastAPI request object
        db: Database session
        
    Returns:
        Redirect to frontend with tokens
    """
    try:
        # Get access token from provider
        token = await oauth.create_client(provider).authorize_access_token(request)
        
        # Extract user info based on provider
        email = None
        full_name = None
        provider_id = None
        photo_url = None
        
        if provider == 'google':
            user_info = token.get('userinfo')
            email = user_info.get('email')
            full_name = user_info.get('name')
            provider_id = user_info.get('sub')
            photo_url = user_info.get('picture')
            
        elif provider == 'facebook':
            # Fetch user info from Facebook Graph API
            resp = await oauth.facebook.get('me?fields=id,name,email,picture')
            user_info = resp.json()
            email = user_info.get('email')
            full_name = user_info.get('name')
            provider_id = user_info.get('id')
            photo_url = user_info.get('picture', {}).get('data', {}).get('url')
            
        elif provider == 'twitter':
            # Twitter v2 API
            resp = await oauth.twitter.get('users/me')
            user_data = resp.json().get('data', {})
            provider_id = user_data.get('id')
            full_name = user_data.get('name')
            # Twitter doesn't provide email in basic scope
            email = f"twitter_{provider_id}@mirai.placeholder"
            photo_url = user_data.get('profile_image_url')
            
        elif provider == 'instagram':
            # Instagram Basic Display API
            resp = await oauth.instagram.get('me?fields=id,username')
            user_data = resp.json()
            provider_id = user_data.get('id')
            full_name = user_data.get('username')
            email = f"instagram_{provider_id}@mirai.placeholder"
        
        if not provider_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user information from provider"
            )
        
        # Find or create user
        result = await db.execute(
            select(User).where(
                User.provider == provider,
                User.provider_user_id == provider_id
            )
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Create new user
            user = User(
                email=email,
                full_name=full_name,
                photo_url=photo_url,
                provider=provider,
                provider_user_id=provider_id,
                subscription_tier=SubscriptionTier.FREE,
                is_active=True,
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow()
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            logger.info(f"New user created via {provider}: {email}")
        else:
            # Update existing user
            user.last_login = datetime.utcnow()
            if photo_url and not user.photo_url:
                user.photo_url = photo_url
            await db.commit()
            logger.info(f"User logged in via {provider}: {email}")
        
        # Generate tokens
        access_token = jwt_handler.create_access_token(data={"sub": str(user.id)})
        refresh_token = jwt_handler.create_refresh_token(data={"sub": str(user.id)})
        
        # Redirect to frontend with tokens
        return RedirectResponse(
            url=f"{FRONTEND_URL}/auth/callback?access_token={access_token}&refresh_token={refresh_token}&provider={provider}"
        )
        
    except Exception as e:
        logger.error(f"OAuth callback error for {provider}: {str(e)}")
        return RedirectResponse(
            url=f"{FRONTEND_URL}/login?error=auth_failed&provider={provider}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        User information
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        photo_url=current_user.photo_url,
        provider=current_user.provider,
        subscription_tier=current_user.subscription_tier,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


@router.post("/logout")
async def logout():
    """
    Logout user.
    Note: With JWT, logout is handled client-side by removing the token.
    This endpoint is provided for consistency and could be extended
    to implement token blacklisting.
    
    Returns:
        Success message
    """
    return {"message": "Successfully logged out"}
