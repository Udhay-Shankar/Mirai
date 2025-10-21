"""
Twitter Scraper using Tweepy (Twitter API v2)
Searches for tweets mentioning a specific keyword
"""
import tweepy
import os
from datetime import datetime, timedelta, timezone
from textblob import TextBlob

class TwitterScraper:
    def __init__(self):
        # Twitter API credentials from environment
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        if self.bearer_token:
            self.client = tweepy.Client(bearer_token=self.bearer_token)
        else:
            self.client = None
            print("[WARNING] Twitter API credentials not found. Please set TWITTER_BEARER_TOKEN in .env")
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text using TextBlob"""
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            return 'positive', polarity
        elif polarity < -0.1:
            return 'negative', polarity
        else:
            return 'neutral', polarity
    
    def search_mentions(self, keyword, max_results=100, days_back=7):
        """
        Search for tweets mentioning the keyword with exact phrase matching
        
        Args:
            keyword: Search term (will search for exact phrase if contains spaces)
            max_results: Maximum tweets to return (default 100, max 100 per request)
            days_back: How many days back to search
            
        Returns:
            List of mention dictionaries with rich metadata
        """
        if not self.client:
            return []
        
        try:
            # Calculate start time - use timezone-aware datetime
            start_time = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days_back)
            
            # Enhance search query for better precision
            # If keyword has spaces or special chars, search as exact phrase
            if ' ' in keyword or len(keyword.split()) > 1:
                search_query = f'"{keyword}"'  # Exact phrase match
            else:
                search_query = keyword
            
            # Add filters to remove retweets and get higher quality content
            search_query += ' -is:retweet lang:en'
            
            # Search tweets
            tweets = self.client.search_recent_tweets(
                query=search_query,
                max_results=min(max_results, 100),
                start_time=start_time,
                tweet_fields=['created_at', 'public_metrics', 'author_id', 'lang', 'geo', 'entities'],
                expansions=['author_id', 'geo.place_id'],
                user_fields=['username', 'name', 'public_metrics', 'verified', 'description', 'location'],
                place_fields=['full_name', 'country']
            )
            
            if not tweets.data:
                return []
            
            # Create user lookup dictionary
            users = {user.id: user for user in tweets.includes.get('users', [])}
            
            # Create place lookup dictionary
            places = {}
            if 'places' in tweets.includes:
                places = {place.id: place for place in tweets.includes['places']}
            
            mentions = []
            for tweet in tweets.data:
                author = users.get(tweet.author_id)
                sentiment, score = self.analyze_sentiment(tweet.text)
                
                # Extract hashtags and mentions
                hashtags = []
                user_mentions = []
                if hasattr(tweet, 'entities') and tweet.entities:
                    if 'hashtags' in tweet.entities:
                        hashtags = [tag['tag'] for tag in tweet.entities['hashtags']]
                    if 'mentions' in tweet.entities:
                        user_mentions = [m['username'] for m in tweet.entities['mentions']]
                
                # Get location data
                location = None
                if hasattr(tweet, 'geo') and tweet.geo and 'place_id' in tweet.geo:
                    place = places.get(tweet.geo['place_id'])
                    if place:
                        location = f"{place.full_name}, {place.country}"
                elif author and hasattr(author, 'location') and author.location:
                    location = author.location
                
                # Calculate influence score (0-100)
                followers = author.public_metrics['followers_count'] if author else 0
                engagement_rate = (tweet.public_metrics['like_count'] + tweet.public_metrics['retweet_count']) / max(followers, 1) * 100
                influence_score = min(100, (followers / 10000) * 50 + engagement_rate * 50)
                
                # Determine source quality
                is_verified = author.verified if author and hasattr(author, 'verified') else False
                source_quality = 'high' if (is_verified or followers > 10000) else ('medium' if followers > 1000 else 'low')
                
                mention = {
                    'platform': 'twitter',
                    'keyword': keyword,
                    'text': tweet.text,
                    'author': author.username if author else 'Unknown',
                    'author_name': author.name if author else 'Unknown',
                    'author_followers': followers,
                    'author_verified': is_verified,
                    'author_bio': author.description[:200] if author and hasattr(author, 'description') and author.description else '',
                    'url': f'https://twitter.com/{author.username}/status/{tweet.id}' if author else '',
                    'timestamp': tweet.created_at.isoformat(),
                    'sentiment': sentiment,
                    'sentiment_score': score,
                    'likes': tweet.public_metrics['like_count'],
                    'retweets': tweet.public_metrics['retweet_count'],
                    'replies': tweet.public_metrics['reply_count'],
                    'engagement': tweet.public_metrics['like_count'] + tweet.public_metrics['retweet_count'] + tweet.public_metrics['reply_count'],
                    'reach': followers + (tweet.public_metrics['retweet_count'] * 100),  # Estimated viral reach
                    'language': tweet.lang,
                    'location': location,
                    'hashtags': hashtags,
                    'mentions': user_mentions,
                    'influence_score': round(influence_score, 2),
                    'source_quality': source_quality,
                    'content_type': 'tweet'
                }
                mentions.append(mention)
            
            print(f"[OK] Found {len(mentions)} tweets for '{keyword}'")
            return mentions
            
        except Exception as e:
            print(f"[ERROR] Twitter scraping error: {str(e)}")
            return []

if __name__ == "__main__":
    # Test the scraper
    from dotenv import load_dotenv
    load_dotenv('../.env')
    
    scraper = TwitterScraper()
    results = scraper.search_mentions("Nike", max_results=10)
    
    for mention in results:
        print(f"\n{mention['author']}: {mention['text'][:100]}...")
        print(f"Sentiment: {mention['sentiment']} ({mention['sentiment_score']:.2f})")
        print(f"Engagement: {mention['engagement']}, Reach: {mention['reach']}")
