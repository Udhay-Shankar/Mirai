"""
Tests for analytics data processing.
"""
import pytest
from datetime import datetime, timedelta
from app.analytics.processor import DataProcessor
from app.analytics.metrics import MetricsCalculator


class TestDataProcessor:
    """Test suite for data processor."""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance."""
        return DataProcessor()
    
    @pytest.fixture
    def sample_mentions(self):
        """Sample mentions data for testing."""
        return [
            {
                "id": "1",
                "text": "Love this #brand! @company is amazing",
                "author_id": "user1",
                "author_name": "User One",
                "author_username": "user1",
                "author_followers": 1000,
                "sentiment": "positive",
                "likes": 50,
                "comments": 10,
                "shares": 5,
                "source": "twitter",
                "language": "en",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "2",
                "text": "Not happy with #brand service",
                "author_id": "user2",
                "author_name": "User Two",
                "author_username": "user2",
                "author_followers": 500,
                "sentiment": "negative",
                "likes": 5,
                "comments": 2,
                "shares": 0,
                "source": "twitter",
                "language": "en",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "3",
                "text": "Just saw #brand mentioned",
                "author_id": "user3",
                "author_name": "User Three",
                "author_username": "user3",
                "author_followers": 2000,
                "sentiment": "neutral",
                "likes": 10,
                "comments": 1,
                "shares": 1,
                "source": "facebook",
                "language": "en",
                "created_at": datetime.now().isoformat()
            }
        ]
    
    def test_extract_hashtags(self, processor):
        """Test hashtag extraction."""
        text = "This is a #test with #multiple #hashtags"
        hashtags = processor.extract_hashtags(text)
        
        assert len(hashtags) == 3
        assert "test" in hashtags
        assert "multiple" in hashtags
        assert "hashtags" in hashtags
    
    def test_extract_mentions(self, processor):
        """Test user mention extraction."""
        text = "Hey @user1 and @user2, check this out!"
        mentions = processor.extract_mentions(text)
        
        assert len(mentions) == 2
        assert "user1" in mentions
        assert "user2" in mentions
    
    def test_calculate_engagement_rate(self, processor):
        """Test engagement rate calculation."""
        mention = {
            "author_followers": 1000,
            "likes": 50,
            "comments": 10,
            "shares": 5
        }
        
        rate = processor.calculate_engagement_rate(mention)
        
        # (50 + 10 + 5) / 1000 * 100 = 6.5%
        assert rate == 6.5
    
    def test_calculate_engagement_rate_zero_followers(self, processor):
        """Test engagement rate with zero followers."""
        mention = {
            "author_followers": 0,
            "likes": 50,
            "comments": 10,
            "shares": 5
        }
        
        rate = processor.calculate_engagement_rate(mention)
        assert rate == 0.0
    
    def test_process_mentions_empty(self, processor):
        """Test processing empty mentions list."""
        result = processor.process_mentions([])
        
        assert result["total_mentions"] == 0
        assert result["unique_authors"] == 0
        assert result["total_reach"] == 0
    
    def test_process_mentions_basic_metrics(self, processor, sample_mentions):
        """Test basic metrics calculation."""
        result = processor.process_mentions(sample_mentions)
        
        assert result["total_mentions"] == 3
        assert result["unique_authors"] == 3
        assert result["total_reach"] == 3500  # 1000 + 500 + 2000
    
    def test_process_mentions_sentiment(self, processor, sample_mentions):
        """Test sentiment breakdown."""
        result = processor.process_mentions(sample_mentions)
        
        sentiment = result["sentiment_breakdown"]
        assert sentiment["positive"] == 1
        assert sentiment["negative"] == 1
        assert sentiment["neutral"] == 1
    
    def test_process_mentions_hashtags(self, processor, sample_mentions):
        """Test hashtag extraction from mentions."""
        result = processor.process_mentions(sample_mentions)
        
        hashtags = result["top_hashtags"]
        assert len(hashtags) > 0
        assert any(tag["tag"] == "brand" for tag in hashtags)
    
    def test_identify_influencers(self, processor, sample_mentions):
        """Test influencer identification."""
        influencers = processor.identify_influencers(
            sample_mentions,
            min_followers=500,
            min_engagement=0.1
        )
        
        # Should identify users with 500+ followers
        assert len(influencers) > 0
        assert all(inf["followers"] >= 500 for inf in influencers)
    
    def test_calculate_trends_daily(self, processor, sample_mentions):
        """Test trend calculation with daily buckets."""
        trends = processor.calculate_trends(sample_mentions, time_buckets='daily')
        
        assert len(trends) > 0
        assert all("timestamp" in trend for trend in trends)
        assert all("count" in trend for trend in trends)
    
    def test_find_similar_creators(self, processor, sample_mentions):
        """Test finding similar creators."""
        similar = processor.find_similar_creators(
            sample_mentions,
            target_keyword="brand",
            min_co_occurrence=1
        )
        
        # Should find creators mentioning similar topics
        assert isinstance(similar, list)


class TestMetricsCalculator:
    """Test suite for metrics calculator."""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator instance."""
        return MetricsCalculator()
    
    @pytest.fixture
    def sample_mentions(self):
        """Sample mentions for metrics testing."""
        return [
            {
                "author_followers": 1000,
                "likes": 100,
                "comments": 20,
                "shares": 10
            },
            {
                "author_followers": 2000,
                "likes": 50,
                "comments": 10,
                "shares": 5
            }
        ]
    
    def test_calculate_engagement_metrics(self, calculator, sample_mentions):
        """Test engagement metrics calculation."""
        metrics = calculator.calculate_engagement_metrics(sample_mentions)
        
        assert metrics["total_likes"] == 150
        assert metrics["total_comments"] == 30
        assert metrics["total_shares"] == 15
        assert metrics["total_engagement"] == 195
    
    def test_calculate_engagement_metrics_empty(self, calculator):
        """Test engagement metrics with empty list."""
        metrics = calculator.calculate_engagement_metrics([])
        
        assert metrics["total_engagement"] == 0
        assert metrics["avg_engagement_per_mention"] == 0
    
    def test_calculate_viral_score(self, calculator):
        """Test viral score calculation."""
        mention = {
            "author_followers": 1000,
            "likes": 500,
            "comments": 100,
            "shares": 50
        }
        
        score = calculator.calculate_viral_score(mention)
        
        # Should be a value between 0 and 100
        assert 0 <= score <= 100
    
    def test_get_top_posts(self, calculator):
        """Test getting top posts."""
        mentions = [
            {
                "id": "1",
                "text": "Viral post",
                "author_name": "Influencer",
                "author_followers": 10000,
                "likes": 5000,
                "comments": 500,
                "shares": 200,
                "source": "twitter",
                "url": "http://example.com/1"
            },
            {
                "id": "2",
                "text": "Regular post",
                "author_name": "User",
                "author_followers": 100,
                "likes": 10,
                "comments": 1,
                "shares": 0,
                "source": "twitter",
                "url": "http://example.com/2"
            }
        ]
        
        top_posts = calculator.get_top_posts(mentions, limit=2)
        
        assert len(top_posts) <= 2
        # First post should have higher viral score
        assert top_posts[0]["viral_score"] > top_posts[1]["viral_score"]


# Performance tests
class TestPerformance:
    """Test performance with large datasets."""
    
    @pytest.fixture
    def processor(self):
        return DataProcessor()
    
    def test_process_large_dataset(self, processor):
        """Test processing large number of mentions."""
        # Create 1000 sample mentions
        large_dataset = []
        for i in range(1000):
            large_dataset.append({
                "id": str(i),
                "text": f"Test mention #{i} #hashtag",
                "author_id": f"user{i % 100}",  # 100 unique users
                "author_followers": 1000,
                "sentiment": "neutral",
                "likes": 10,
                "comments": 2,
                "shares": 1,
                "source": "twitter",
                "language": "en",
                "created_at": datetime.now().isoformat()
            })
        
        # Should complete without errors
        result = processor.process_mentions(large_dataset)
        
        assert result["total_mentions"] == 1000
        assert result["unique_authors"] == 100
