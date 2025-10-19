"""
Analytics router for social listening data and insights.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging

from app.models import User, SubscriptionTier
from app.auth.dependencies_jwt import get_current_user, get_current_premium_user
from app.awario.client import awario_client
from app.awario.exceptions import AwarioException
from app.analytics.processor import data_processor
from app.analytics.metrics import metrics_calculator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


class AnalyticsRequest(BaseModel):
    """Request model for analytics queries."""
    keyword: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    alert_id: Optional[str] = None


class BasicStatsResponse(BaseModel):
    """Basic stats response for free users."""
    keyword: str
    date_range: Dict[str, str]
    total_mentions: int
    sentiment_breakdown: Dict[str, int]
    top_keywords: List[Dict[str, Any]]
    sources: Dict[str, int]
    message: Optional[str] = None


class PremiumStatsResponse(BaseModel):
    """Premium stats response with full analytics."""
    keyword: str
    date_range: Dict[str, str]
    
    # Basic metrics
    total_mentions: int
    unique_authors: int
    total_reach: int
    average_sentiment: float
    sentiment_breakdown: Dict[str, int]
    
    # Detailed breakdowns
    top_keywords: List[Dict[str, Any]]
    top_hashtags: List[Dict[str, Any]]
    top_mentions: List[Dict[str, Any]]
    sources: Dict[str, int]
    languages: Dict[str, int]
    
    # Engagement metrics
    engagement_metrics: Dict[str, Any]
    
    # Trends
    trends: List[Dict[str, Any]]
    
    # Top posts
    top_posts: List[Dict[str, Any]]


def filter_response_by_tier(
    user: User,
    full_data: Dict[str, Any],
    keyword: str,
    date_range: Dict[str, str]
) -> Dict[str, Any]:
    """
    Filter analytics response based on user subscription tier.
    
    Args:
        user: Current user
        full_data: Complete analytics data
        keyword: Search keyword
        date_range: Date range dict
        
    Returns:
        Filtered response based on subscription
    """
    if user.is_premium():
        return full_data
    
    # Free tier: return limited data
    return {
        "keyword": keyword,
        "date_range": date_range,
        "total_mentions": full_data.get("total_mentions", 0),
        "sentiment_breakdown": full_data.get("sentiment_breakdown", {}),
        "top_keywords": full_data.get("top_hashtags", [])[:5],  # Only top 5
        "sources": full_data.get("sources", {}),
        "message": "Upgrade to Premium for full analytics, trends, and influencer data"
    }


@router.post("/search", response_model=Dict)
async def search_mentions(
    request: AnalyticsRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Search for mentions and get analytics.
    Returns basic stats for free users, full analytics for premium.
    
    Args:
        request: Analytics request
        current_user: Authenticated user
        
    Returns:
        Analytics data based on subscription tier
    """
    try:
        # Set default date range
        if not request.start_date:
            # Free users: 7 days, Premium: 30 days
            days_back = 7 if not current_user.is_premium() else 30
            request.start_date = datetime.now() - timedelta(days=days_back)
        
        if not request.end_date:
            request.end_date = datetime.now()
        
        date_range = {
            "start": request.start_date.isoformat(),
            "end": request.end_date.isoformat()
        }
        
        # Fetch mentions from Awario
        logger.info(f"Fetching mentions for keyword: {request.keyword}")
        mentions_data = await awario_client.get_mentions(
            keyword=request.keyword,
            alert_id=request.alert_id,
            start_date=request.start_date,
            end_date=request.end_date,
            page_size=100
        )
        
        mentions = mentions_data.get('mentions', [])
        
        # Process basic metrics
        basic_metrics = data_processor.process_mentions(mentions)
        
        # Build full response
        full_data = {
            "keyword": request.keyword,
            "date_range": date_range,
            **basic_metrics
        }
        
        # Add premium features if user has access
        if current_user.is_premium():
            # Calculate engagement metrics
            engagement = metrics_calculator.calculate_engagement_metrics(mentions)
            full_data["engagement_metrics"] = engagement
            
            # Calculate trends
            trends = data_processor.calculate_trends(mentions, time_buckets='daily')
            full_data["trends"] = trends
            
            # Get top posts
            top_posts = metrics_calculator.get_top_posts(mentions, limit=10)
            full_data["top_posts"] = top_posts
        
        # Filter based on tier
        response = filter_response_by_tier(
            current_user,
            full_data,
            request.keyword,
            date_range
        )
        
        return response
        
    except AwarioException as e:
        logger.error(f"Awario API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Social listening service error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error in search_mentions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )


@router.get("/influencers")
async def get_influencers(
    keyword: str = Query(..., description="Keyword to search for"),
    min_followers: int = Query(1000, description="Minimum follower count"),
    limit: int = Query(20, description="Number of influencers to return"),
    current_user: User = Depends(get_current_premium_user)
):
    """
    Get top influencers mentioning the keyword.
    Premium feature only.
    
    Args:
        keyword: Search keyword
        min_followers: Minimum follower count
        limit: Max results
        current_user: Authenticated premium user
        
    Returns:
        List of influencers
    """
    try:
        # Fetch mentions
        mentions_data = await awario_client.get_mentions(
            keyword=keyword,
            start_date=datetime.now() - timedelta(days=30),
            page_size=100
        )
        
        mentions = mentions_data.get('mentions', [])
        
        # Identify influencers
        influencers = data_processor.identify_influencers(
            mentions,
            min_followers=min_followers,
            min_engagement=0.1
        )
        
        return {
            "keyword": keyword,
            "total_influencers": len(influencers),
            "influencers": influencers[:limit]
        }
        
    except AwarioException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service error: {str(e)}"
        )


@router.get("/trending")
async def get_trending_topics(
    keyword: str = Query(..., description="Keyword to search for"),
    limit: int = Query(20, description="Number of trending topics"),
    current_user: User = Depends(get_current_premium_user)
):
    """
    Get trending topics and hashtags.
    Premium feature only.
    
    Args:
        keyword: Search keyword
        limit: Max results
        current_user: Authenticated premium user
        
    Returns:
        Trending topics data
    """
    try:
        trending_data = await awario_client.get_trending_topics(
            keyword=keyword,
            limit=limit
        )
        
        return trending_data
        
    except AwarioException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service error: {str(e)}"
        )


@router.post("/competitors")
async def compare_competitors(
    primary_keyword: str = Query(..., description="Primary keyword"),
    competitors: List[str] = Query(..., description="Competitor keywords"),
    current_user: User = Depends(get_current_premium_user)
):
    """
    Compare primary keyword against competitors.
    Premium feature only.
    
    Args:
        primary_keyword: Primary keyword to track
        competitors: List of competitor keywords
        current_user: Authenticated premium user
        
    Returns:
        Competitor comparison data
    """
    try:
        # Fetch primary mentions
        primary_data = await awario_client.get_mentions(
            keyword=primary_keyword,
            start_date=datetime.now() - timedelta(days=30),
            page_size=100
        )
        primary_mentions = primary_data.get('mentions', [])
        
        # Fetch competitor mentions
        competitor_mentions = {}
        for competitor in competitors[:5]:  # Limit to 5 competitors
            comp_data = await awario_client.get_mentions(
                keyword=competitor,
                start_date=datetime.now() - timedelta(days=30),
                page_size=100
            )
            competitor_mentions[competitor] = comp_data.get('mentions', [])
        
        # Compare
        comparison = metrics_calculator.compare_competitors(
            primary_mentions,
            competitor_mentions
        )
        
        return comparison
        
    except AwarioException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service error: {str(e)}"
        )


@router.get("/similar-creators")
async def find_similar_creators(
    keyword: str = Query(..., description="Keyword to search for"),
    min_co_occurrence: int = Query(3, description="Minimum co-occurrences"),
    current_user: User = Depends(get_current_premium_user)
):
    """
    Find similar or rising content creators.
    Premium feature only.
    
    Args:
        keyword: Search keyword
        min_co_occurrence: Minimum co-occurrences threshold
        current_user: Authenticated premium user
        
    Returns:
        Similar creators data
    """
    try:
        # Fetch mentions
        mentions_data = await awario_client.get_mentions(
            keyword=keyword,
            start_date=datetime.now() - timedelta(days=30),
            page_size=100
        )
        
        mentions = mentions_data.get('mentions', [])
        
        # Find similar creators
        similar = data_processor.find_similar_creators(
            mentions,
            target_keyword=keyword,
            min_co_occurrence=min_co_occurrence
        )
        
        # Detect rising creators
        rising = data_processor.detect_rising_creators(
            mentions,
            lookback_days=30
        )
        
        return {
            "keyword": keyword,
            "similar_creators": similar[:20],
            "rising_creators": rising[:20]
        }
        
    except AwarioException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service error: {str(e)}"
        )


@router.get("/demographics")
async def get_demographics(
    keyword: str = Query(..., description="Keyword to search for"),
    current_user: User = Depends(get_current_premium_user)
):
    """
    Get demographic breakdown of mentions.
    Premium feature only.
    
    Args:
        keyword: Search keyword
        current_user: Authenticated premium user
        
    Returns:
        Demographic data
    """
    try:
        # Fetch mentions
        mentions_data = await awario_client.get_mentions(
            keyword=keyword,
            start_date=datetime.now() - timedelta(days=30),
            page_size=100
        )
        
        mentions = mentions_data.get('mentions', [])
        
        # Calculate demographics
        demographics = metrics_calculator.calculate_demographic_breakdown(mentions)
        
        return {
            "keyword": keyword,
            "demographics": demographics
        }
        
    except AwarioException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service error: {str(e)}"
        )
