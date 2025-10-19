"""
Awario API client for social listening data.
Implements API wrappers for creating alerts, fetching mentions, and getting insights.
"""
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from app.config import settings
from app.awario.exceptions import (
    AwarioAuthenticationError,
    AwarioRateLimitError,
    AwarioAPIError,
    AwarioNetworkError,
    AwarioValidationError
)

logger = logging.getLogger(__name__)


class AwarioClient:
    """Client for interacting with Awario API."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Awario API client.
        
        Args:
            api_key: Awario API key (defaults to settings if not provided)
        """
        self.api_key = api_key or settings.awario_api_key
        self.base_url = settings.awario_base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict:
        """
        Make HTTP request to Awario API with error handling.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            
        Returns:
            API response as dictionary
            
        Raises:
            AwarioException: On API errors
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=data
                )
                
                # Handle different status codes
                if response.status_code == 401:
                    raise AwarioAuthenticationError("Invalid API key or authentication failed")
                
                elif response.status_code == 429:
                    raise AwarioRateLimitError("API rate limit exceeded")
                
                elif response.status_code >= 400:
                    error_data = response.json() if response.text else {}
                    raise AwarioAPIError(
                        f"API request failed: {error_data.get('message', 'Unknown error')}",
                        status_code=response.status_code,
                        response_data=error_data
                    )
                
                return response.json()
                
        except httpx.TimeoutException:
            raise AwarioNetworkError("Request timed out")
        except httpx.NetworkError as e:
            raise AwarioNetworkError(f"Network error: {str(e)}")
        except Exception as e:
            if isinstance(e, (AwarioAuthenticationError, AwarioRateLimitError, AwarioAPIError)):
                raise
            logger.error(f"Unexpected error in API request: {str(e)}")
            raise AwarioAPIError(f"Unexpected error: {str(e)}")
    
    async def create_alert(
        self,
        keyword: str,
        alert_name: Optional[str] = None,
        languages: Optional[List[str]] = None,
        locations: Optional[List[str]] = None
    ) -> Dict:
        """
        Create a new alert for monitoring mentions.
        
        Args:
            keyword: Keyword or brand name to monitor
            alert_name: Custom name for the alert
            languages: List of language codes to monitor
            locations: List of location codes to monitor
            
        Returns:
            Alert creation response with alert_id
        """
        if not keyword or not keyword.strip():
            raise AwarioValidationError("Keyword cannot be empty")
        
        data = {
            "name": alert_name or f"Alert for {keyword}",
            "query": keyword,
            "languages": languages or ["en"],
            "sources": ["twitter", "facebook", "instagram", "youtube", "reddit", "news"]
        }
        
        if locations:
            data["locations"] = locations
        
        logger.info(f"Creating alert for keyword: {keyword}")
        return await self._make_request("POST", "/alerts", data=data)
    
    async def get_mentions(
        self,
        alert_id: str = None,
        keyword: str = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 50,
        sort_by: str = "date",
        sentiment: Optional[str] = None
    ) -> Dict:
        """
        Fetch mentions for a keyword or alert.
        
        Args:
            alert_id: Awario alert ID
            keyword: Direct keyword search (if no alert_id)
            start_date: Start date for mentions
            end_date: End date for mentions
            page: Page number for pagination
            page_size: Number of results per page
            sort_by: Sort order (date, reach, engagement)
            sentiment: Filter by sentiment (positive, negative, neutral)
            
        Returns:
            Dictionary containing mentions data with pagination info
        """
        if not alert_id and not keyword:
            raise AwarioValidationError("Either alert_id or keyword must be provided")
        
        # Default date range: last 30 days
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        params = {
            "page": page,
            "page_size": min(page_size, 100),  # Cap at 100
            "sort_by": sort_by,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
        if alert_id:
            params["alert_id"] = alert_id
        else:
            params["keyword"] = keyword
        
        if sentiment:
            params["sentiment"] = sentiment
        
        logger.info(f"Fetching mentions for alert_id={alert_id}, keyword={keyword}")
        return await self._make_request("GET", "/mentions", params=params)
    
    async def get_sentiment_analysis(
        self,
        alert_id: str = None,
        keyword: str = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get sentiment analysis for mentions.
        
        Args:
            alert_id: Awario alert ID
            keyword: Direct keyword search
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            Sentiment breakdown and analysis
        """
        if not alert_id and not keyword:
            raise AwarioValidationError("Either alert_id or keyword must be provided")
        
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
        if alert_id:
            params["alert_id"] = alert_id
        else:
            params["keyword"] = keyword
        
        return await self._make_request("GET", "/analytics/sentiment", params=params)
    
    async def get_influencers(
        self,
        alert_id: str = None,
        keyword: str = None,
        min_followers: int = 1000,
        limit: int = 50
    ) -> Dict:
        """
        Get top influencers mentioning the keyword.
        
        Args:
            alert_id: Awario alert ID
            keyword: Direct keyword search
            min_followers: Minimum follower count for influencers
            limit: Maximum number of influencers to return
            
        Returns:
            List of influencers with metrics
        """
        if not alert_id and not keyword:
            raise AwarioValidationError("Either alert_id or keyword must be provided")
        
        params = {
            "min_followers": min_followers,
            "limit": min(limit, 100)
        }
        
        if alert_id:
            params["alert_id"] = alert_id
        else:
            params["keyword"] = keyword
        
        return await self._make_request("GET", "/analytics/influencers", params=params)
    
    async def get_reach_stats(
        self,
        alert_id: str = None,
        keyword: str = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get reach statistics for mentions.
        
        Args:
            alert_id: Awario alert ID
            keyword: Direct keyword search
            start_date: Start date for stats
            end_date: End date for stats
            
        Returns:
            Reach statistics including total reach, potential impressions
        """
        if not alert_id and not keyword:
            raise AwarioValidationError("Either alert_id or keyword must be provided")
        
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
        if alert_id:
            params["alert_id"] = alert_id
        else:
            params["keyword"] = keyword
        
        return await self._make_request("GET", "/analytics/reach", params=params)
    
    async def get_trending_topics(
        self,
        alert_id: str = None,
        keyword: str = None,
        limit: int = 20
    ) -> Dict:
        """
        Get trending topics, hashtags, and keywords.
        
        Args:
            alert_id: Awario alert ID
            keyword: Direct keyword search
            limit: Number of trending items to return
            
        Returns:
            List of trending topics with frequency
        """
        if not alert_id and not keyword:
            raise AwarioValidationError("Either alert_id or keyword must be provided")
        
        params = {"limit": min(limit, 50)}
        
        if alert_id:
            params["alert_id"] = alert_id
        else:
            params["keyword"] = keyword
        
        return await self._make_request("GET", "/analytics/trending", params=params)
    
    async def get_source_breakdown(
        self,
        alert_id: str = None,
        keyword: str = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get breakdown of mentions by source (platform).
        
        Args:
            alert_id: Awario alert ID
            keyword: Direct keyword search
            start_date: Start date
            end_date: End date
            
        Returns:
            Breakdown by social media platform
        """
        if not alert_id and not keyword:
            raise AwarioValidationError("Either alert_id or keyword must be provided")
        
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
        if alert_id:
            params["alert_id"] = alert_id
        else:
            params["keyword"] = keyword
        
        return await self._make_request("GET", "/analytics/sources", params=params)


# Global Awario client instance
awario_client = AwarioClient()
