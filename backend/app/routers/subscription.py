"""
Subscription management router.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging

from app.database import get_db
from app.models import User, SubscriptionTier
from app.auth.dependencies_jwt import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/subscription", tags=["Subscription"])


class SubscriptionResponse(BaseModel):
    """Subscription status response."""
    tier: SubscriptionTier
    is_premium: bool
    start_date: datetime = None
    end_date: datetime = None
    days_remaining: int = None


class UpgradeRequest(BaseModel):
    """Subscription upgrade request."""
    tier: SubscriptionTier
    payment_token: str = None  # For payment processing


@router.get("/status", response_model=SubscriptionResponse)
async def get_subscription_status(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's subscription status.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Subscription information
    """
    days_remaining = None
    
    if current_user.subscription_end_date:
        remaining = current_user.subscription_end_date - datetime.now()
        days_remaining = max(0, remaining.days)
    
    return SubscriptionResponse(
        tier=current_user.subscription_tier,
        is_premium=current_user.is_premium(),
        start_date=current_user.subscription_start_date,
        end_date=current_user.subscription_end_date,
        days_remaining=days_remaining
    )


@router.post("/upgrade", response_model=SubscriptionResponse)
async def upgrade_subscription(
    request: UpgradeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upgrade user subscription.
    
    Args:
        request: Upgrade request with tier
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Updated subscription information
    """
    if request.tier == SubscriptionTier.FREE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot upgrade to free tier"
        )
    
    # In a real app, you would:
    # 1. Verify payment_token with payment processor
    # 2. Process payment
    # 3. Update subscription on success
    
    # For demo purposes, we'll just update the subscription
    current_user.subscription_tier = request.tier
    current_user.subscription_start_date = datetime.now()
    
    # Set expiration (e.g., 30 days for monthly)
    if request.tier == SubscriptionTier.PREMIUM:
        current_user.subscription_end_date = datetime.now() + timedelta(days=30)
    elif request.tier == SubscriptionTier.ENTERPRISE:
        current_user.subscription_end_date = datetime.now() + timedelta(days=365)
    
    await db.commit()
    await db.refresh(current_user)
    
    logger.info(f"User {current_user.id} upgraded to {request.tier}")
    
    days_remaining = None
    if current_user.subscription_end_date:
        remaining = current_user.subscription_end_date - datetime.now()
        days_remaining = max(0, remaining.days)
    
    return SubscriptionResponse(
        tier=current_user.subscription_tier,
        is_premium=current_user.is_premium(),
        start_date=current_user.subscription_start_date,
        end_date=current_user.subscription_end_date,
        days_remaining=days_remaining
    )


@router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel user subscription.
    Reverts to free tier.
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Cancellation confirmation
    """
    if current_user.subscription_tier == SubscriptionTier.FREE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription to cancel"
        )
    
    # In a real app, you would:
    # 1. Cancel recurring billing with payment processor
    # 2. Set subscription to expire at end of current period
    
    # For demo, immediately revert to free
    current_user.subscription_tier = SubscriptionTier.FREE
    current_user.subscription_end_date = None
    
    await db.commit()
    
    logger.info(f"User {current_user.id} cancelled subscription")
    
    return {
        "message": "Subscription cancelled successfully",
        "tier": SubscriptionTier.FREE
    }


@router.get("/features")
async def get_features():
    """
    Get list of features by subscription tier.
    
    Returns:
        Feature comparison
    """
    return {
        "free": {
            "tier": "free",
            "price": "$0/month",
            "features": [
                "Basic mention tracking (last 7 days)",
                "Sentiment analysis",
                "Top 5 keywords",
                "Source breakdown",
                "Limited to 1 keyword"
            ]
        },
        "premium": {
            "tier": "premium",
            "price": "$29/month",
            "features": [
                "All Free features",
                "Extended history (30+ days)",
                "Full influencer lists",
                "Trend analysis & time series",
                "Engagement metrics",
                "Top posts by virality",
                "Up to 10 keywords",
                "Export data"
            ]
        },
        "enterprise": {
            "tier": "enterprise",
            "price": "$99/month",
            "features": [
                "All Premium features",
                "Unlimited keywords",
                "Competitor comparison",
                "Demographic breakdowns",
                "Similar & rising creator discovery",
                "API access",
                "Priority support",
                "Custom reports"
            ]
        }
    }
