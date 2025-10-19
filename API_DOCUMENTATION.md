# Mirai API Documentation

## Base URL
```
Development: http://localhost:8000
Production: https://api.mirai.app
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <firebase_token>
```

## Endpoints

### Authentication

#### POST /api/auth/register
Register a new user or login existing user.

**Request Body:**
```json
{
  "firebase_token": "string",
  "provider": "google|facebook|email|phone"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Doe",
  "provider": "google",
  "subscription_tier": "free",
  "is_premium": false,
  "created_at": "2024-01-01T00:00:00"
}
```

#### GET /api/auth/me
Get current user information.

**Headers:** Authorization required

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Doe",
  "subscription_tier": "premium",
  "is_premium": true
}
```

#### POST /api/auth/logout
Logout current user and revoke tokens.

**Headers:** Authorization required

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

---

### Analytics

#### POST /api/analytics/search
Search for mentions and get analytics data.

**Headers:** Authorization required

**Request Body:**
```json
{
  "keyword": "Nike",
  "start_date": "2024-01-01T00:00:00",  // Optional
  "end_date": "2024-01-31T23:59:59",    // Optional
  "alert_id": "string"                   // Optional
}
```

**Response (Free Tier):**
```json
{
  "keyword": "Nike",
  "date_range": {
    "start": "2024-01-01T00:00:00",
    "end": "2024-01-07T23:59:59"
  },
  "total_mentions": 1234,
  "sentiment_breakdown": {
    "positive": 500,
    "negative": 234,
    "neutral": 500
  },
  "top_keywords": [
    {"tag": "running", "count": 150},
    {"tag": "shoes", "count": 120}
  ],
  "sources": {
    "twitter": 600,
    "facebook": 400,
    "instagram": 234
  },
  "message": "Upgrade to Premium for full analytics..."
}
```

**Response (Premium Tier):**
```json
{
  "keyword": "Nike",
  "date_range": {
    "start": "2024-01-01T00:00:00",
    "end": "2024-01-31T23:59:59"
  },
  "total_mentions": 5678,
  "unique_authors": 3456,
  "total_reach": 2500000,
  "average_sentiment": 0.35,
  "sentiment_breakdown": {
    "positive": 2500,
    "negative": 678,
    "neutral": 2500
  },
  "top_hashtags": [...],
  "top_mentions": [...],
  "sources": {...},
  "languages": {...},
  "engagement_metrics": {
    "total_likes": 50000,
    "total_comments": 10000,
    "total_shares": 5000,
    "total_engagement": 65000,
    "avg_engagement_per_mention": 11.5,
    "engagement_rate": 2.6
  },
  "trends": [
    {
      "timestamp": "2024-01-01T00:00:00",
      "count": 150,
      "reach": 80000,
      "sentiment": {
        "positive": 80,
        "negative": 20,
        "neutral": 50
      }
    }
  ],
  "top_posts": [...]
}
```

#### GET /api/analytics/influencers
Get top influencers mentioning the keyword. **Premium only.**

**Headers:** Authorization required

**Query Parameters:**
- `keyword` (required): Search keyword
- `min_followers` (optional, default: 1000): Minimum follower count
- `limit` (optional, default: 20): Number of results

**Response:**
```json
{
  "keyword": "Nike",
  "total_influencers": 45,
  "influencers": [
    {
      "author_id": "123456",
      "author_name": "John Runner",
      "author_username": "johnrunner",
      "followers": 150000,
      "mention_count": 5,
      "total_engagement": 5000,
      "avg_engagement_rate": 3.5,
      "profile_url": "https://twitter.com/johnrunner",
      "verified": true
    }
  ]
}
```

#### GET /api/analytics/trending
Get trending topics and hashtags. **Premium only.**

**Headers:** Authorization required

**Query Parameters:**
- `keyword` (required): Search keyword
- `limit` (optional, default: 20): Number of results

**Response:**
```json
{
  "keyword": "Nike",
  "trending": [
    {
      "topic": "AirMax",
      "count": 450,
      "growth_rate": 25.5
    }
  ]
}
```

#### POST /api/analytics/competitors
Compare keyword against competitors. **Premium only.**

**Headers:** Authorization required

**Query Parameters:**
- `primary_keyword` (required): Primary keyword
- `competitors` (required): List of competitor keywords

**Response:**
```json
{
  "primary": {
    "keyword": "Nike",
    "total_mentions": 5000,
    "share_of_voice": 45.5
  },
  "competitors": [
    {
      "keyword": "Adidas",
      "total_mentions": 4000,
      "share_of_voice": 36.4
    }
  ],
  "summary": {
    "total_tracked_mentions": 11000,
    "primary_rank": 1
  }
}
```

#### GET /api/analytics/similar-creators
Find similar or rising content creators. **Premium only.**

**Headers:** Authorization required

**Query Parameters:**
- `keyword` (required): Search keyword
- `min_co_occurrence` (optional, default: 3): Minimum co-occurrences

**Response:**
```json
{
  "keyword": "Nike",
  "similar_creators": [...],
  "rising_creators": [
    {
      "author_id": "789",
      "author_name": "New Runner",
      "followers": 5000,
      "early_mentions": 2,
      "recent_mentions": 10,
      "growth_rate": 400.0,
      "is_new": false
    }
  ]
}
```

#### GET /api/analytics/demographics
Get demographic breakdown. **Premium only.**

**Headers:** Authorization required

**Query Parameters:**
- `keyword` (required): Search keyword

**Response:**
```json
{
  "keyword": "Nike",
  "demographics": {
    "gender": {
      "male": 60.5,
      "female": 35.2,
      "other": 4.3
    },
    "age_groups": {
      "18-24": 35.0,
      "25-34": 40.0,
      "35-44": 15.0,
      "45-54": 7.0,
      "55+": 3.0
    },
    "top_locations": {
      "United States": 1500,
      "United Kingdom": 800,
      "Canada": 600
    }
  }
}
```

---

### Subscription

#### GET /api/subscription/status
Get current user's subscription status.

**Headers:** Authorization required

**Response:**
```json
{
  "tier": "premium",
  "is_premium": true,
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-02-01T00:00:00",
  "days_remaining": 15
}
```

#### POST /api/subscription/upgrade
Upgrade user subscription.

**Headers:** Authorization required

**Request Body:**
```json
{
  "tier": "premium",
  "payment_token": "tok_visa_123"  // Optional for demo
}
```

**Response:**
```json
{
  "tier": "premium",
  "is_premium": true,
  "start_date": "2024-01-15T00:00:00",
  "end_date": "2024-02-15T00:00:00",
  "days_remaining": 30
}
```

#### POST /api/subscription/cancel
Cancel user subscription.

**Headers:** Authorization required

**Response:**
```json
{
  "message": "Subscription cancelled successfully",
  "tier": "free"
}
```

#### GET /api/subscription/features
Get feature comparison for all tiers.

**Response:**
```json
{
  "free": {
    "tier": "free",
    "price": "$0/month",
    "features": [...]
  },
  "premium": {
    "tier": "premium",
    "price": "$29/month",
    "features": [...]
  },
  "enterprise": {
    "tier": "enterprise",
    "price": "$99/month",
    "features": [...]
  }
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Validation error",
  "errors": [...]
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "detail": "Premium subscription required for this feature"
}
```

### 404 Not Found
```json
{
  "detail": "User not found in database"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "message": "An unexpected error occurred"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Social listening service error",
  "message": "Awario API connection failed"
}
```

---

## Rate Limiting

API requests are rate limited to:
- **Free tier**: 60 requests per minute
- **Premium tier**: 120 requests per minute
- **Enterprise tier**: Unlimited

---

## Pagination

Endpoints that return lists support pagination:

**Query Parameters:**
- `page` (default: 1): Page number
- `page_size` (default: 20, max: 100): Items per page

**Response includes:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

## Webhooks (Coming Soon)

Subscribe to real-time mention notifications.

---

## SDKs

Official SDKs available for:
- Python
- JavaScript/TypeScript
- Java
- Ruby

---

## Support

For API support:
- Documentation: https://docs.mirai.app
- Email: api@mirai.app
- Status: https://status.mirai.app
