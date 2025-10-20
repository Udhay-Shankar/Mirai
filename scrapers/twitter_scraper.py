"""
Twitter Scraper using Tweepy (Twitter API v2)
Searches for tweets mentioning a specific keyword
"""
import tweepy
import os
from datetime import datetime, timedelta
from textblob import TextBlob

class TwitterScraper:
    def __init__(self):
        # Twitter API credentials from environment
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        if self.bearer_token:
            self.client = tweepy.Client(bearer_token=self.bearer_token)
        else:
            self.client = None
            print("⚠️  Twitter API credentials not found. Please set TWITTER_BEARER_TOKEN in .env")
    
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
        Search for tweets mentioning the keyword
        
        Args:
            keyword: Search term
            max_results: Maximum tweets to return (default 100, max 100 per request)
            days_back: How many days back to search
            
        Returns:
            List of mention dictionaries
        """
        if not self.client:
            return []
        
        try:
            # Calculate start time (7 days ago by default)
            start_time = datetime.utcnow() - timedelta(days=days_back)
            
            # Search tweets
            tweets = self.client.search_recent_tweets(
                query=keyword,
                max_results=min(max_results, 100),
                start_time=start_time,
                tweet_fields=['created_at', 'public_metrics', 'author_id', 'lang'],
                expansions=['author_id'],
                user_fields=['username', 'name', 'public_metrics']
            )
            
            if not tweets.data:
                return []
            
            # Create user lookup dictionary
            users = {user.id: user for user in tweets.includes.get('users', [])}
            
            mentions = []
            for tweet in tweets.data:
                author = users.get(tweet.author_id)
                sentiment, score = self.analyze_sentiment(tweet.text)
                
                mention = {
                    'platform': 'twitter',
                    'keyword': keyword,
                    'text': tweet.text,
                    'author': author.username if author else 'Unknown',
                    'author_name': author.name if author else 'Unknown',
                    'author_followers': author.public_metrics['followers_count'] if author else 0,
                    'url': f'https://twitter.com/{author.username}/status/{tweet.id}' if author else '',
                    'timestamp': tweet.created_at.isoformat(),
                    'sentiment': sentiment,
                    'sentiment_score': score,
                    'likes': tweet.public_metrics['like_count'],
                    'retweets': tweet.public_metrics['retweet_count'],
                    'replies': tweet.public_metrics['reply_count'],
                    'engagement': tweet.public_metrics['like_count'] + tweet.public_metrics['retweet_count'],
                    'reach': author.public_metrics['followers_count'] if author else 0,
                    'language': tweet.lang
                }
                mentions.append(mention)
            
            print(f"✅ Found {len(mentions)} tweets for '{keyword}'")
            return mentions
            
        except Exception as e:
            print(f"❌ Twitter scraping error: {str(e)}")
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
