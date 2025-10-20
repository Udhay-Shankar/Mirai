"""
Reddit Scraper using PRAW (Python Reddit API Wrapper)
Searches for posts and comments mentioning a specific keyword
"""
import praw
import os
from datetime import datetime
from textblob import TextBlob

class RedditScraper:
    def __init__(self):
        # Reddit API credentials from environment
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'Mirai Social Listening v1.0')
        
        if self.client_id and self.client_secret:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
        else:
            self.reddit = None
            print("⚠️  Reddit API credentials not found. Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env")
    
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
    
    def search_mentions(self, keyword, limit=100, time_filter='week'):
        """
        Search for Reddit posts mentioning the keyword
        
        Args:
            keyword: Search term
            limit: Maximum results to return
            time_filter: 'hour', 'day', 'week', 'month', 'year', 'all'
            
        Returns:
            List of mention dictionaries
        """
        if not self.reddit:
            return []
        
        try:
            mentions = []
            
            # Search all of Reddit
            for submission in self.reddit.subreddit('all').search(keyword, limit=limit, time_filter=time_filter):
                sentiment, score = self.analyze_sentiment(submission.title + ' ' + submission.selftext)
                
                mention = {
                    'platform': 'reddit',
                    'keyword': keyword,
                    'text': f"{submission.title}\n{submission.selftext[:200]}",
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'author_name': str(submission.author) if submission.author else '[deleted]',
                    'author_followers': 0,  # Reddit doesn't expose follower count easily
                    'url': f'https://reddit.com{submission.permalink}',
                    'timestamp': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'sentiment': sentiment,
                    'sentiment_score': score,
                    'likes': submission.score,
                    'comments': submission.num_comments,
                    'engagement': submission.score + submission.num_comments,
                    'reach': submission.score * 10,  # Estimated reach
                    'subreddit': submission.subreddit.display_name
                }
                mentions.append(mention)
            
            print(f"✅ Found {len(mentions)} Reddit posts for '{keyword}'")
            return mentions
            
        except Exception as e:
            print(f"❌ Reddit scraping error: {str(e)}")
            return []

if __name__ == "__main__":
    # Test the scraper
    from dotenv import load_dotenv
    load_dotenv('../.env')
    
    scraper = RedditScraper()
    results = scraper.search_mentions("Nike", limit=10)
    
    for mention in results:
        print(f"\n{mention['author']} in r/{mention['subreddit']}")
        print(f"{mention['text'][:100]}...")
        print(f"Sentiment: {mention['sentiment']} | Score: {mention['likes']} | Comments: {mention['comments']}")
