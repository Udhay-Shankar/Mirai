"""
Reddit Scraper using Reddit JSON API (NO authentication required!)
Searches for posts mentioning a specific keyword
"""
import requests
import os
from datetime import datetime
from textblob import TextBlob
import time

class RedditScraper:
    def __init__(self):
        # Reddit JSON API - no auth needed for public posts!
        self.base_url = "https://www.reddit.com"
        self.headers = {
            'User-Agent': 'Mirai Social Listening v1.0'
        }
    
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
    
    def search_mentions(self, keyword, limit=100):
        """
        Search for Reddit posts mentioning the keyword using JSON API with exact matching
        
        Args:
            keyword: Search term (will match exact phrase if contains spaces)
            limit: Maximum posts to return
            
        Returns:
            List of mention dictionaries with rich metadata
        """
        try:
            mentions = []
            
            # Search Reddit using JSON API
            search_url = f"{self.base_url}/search.json"
            
            # Enhance search query for exact phrase matching
            if ' ' in keyword or len(keyword.split()) > 1:
                search_term = f'"{keyword}"'  # Exact phrase
            else:
                search_term = keyword
            
            params = {
                'q': search_term,
                'limit': min(limit, 100),
                'sort': 'new',
                't': 'week'  # Past week
            }
            
            response = requests.get(search_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' not in data or 'children' not in data['data']:
                return []
            
            for post in data['data']['children']:
                post_data = post['data']
                
                # Skip if keyword not in title or selftext (strict filtering)
                title = post_data.get('title', '').lower()
                selftext = post_data.get('selftext', '').lower()
                keyword_lower = keyword.lower()
                
                # STRICT: Always ensure exact keyword appears (even for single words)
                # This prevents "StratSchool" from matching "Stratocaster" or "school"
                if keyword_lower not in title and keyword_lower not in selftext:
                    continue
                
                # Combine title and selftext for sentiment analysis
                text = f"{post_data.get('title', '')} {post_data.get('selftext', '')}"
                sentiment, score = self.analyze_sentiment(text)
                
                # Extract awards count
                awards = post_data.get('total_awards_received', 0)
                
                # Calculate influence score
                karma = post_data.get('ups', 0)
                comments = post_data.get('num_comments', 0)
                influence_score = min(100, (karma / 100) * 50 + (comments / 50) * 50)
                
                # Determine source quality based on subreddit and karma
                source_quality = 'high' if karma > 100 else ('medium' if karma > 10 else 'low')
                
                # Get subreddit info
                subreddit = post_data.get('subreddit', 'Unknown')
                subreddit_subscribers = post_data.get('subreddit_subscribers', 0)
                
                mention = {
                    'platform': 'reddit',
                    'keyword': keyword,
                    'text': post_data.get('title', ''),
                    'full_text': text[:500],  # Store longer text for analysis
                    'author': post_data.get('author', 'Unknown'),
                    'author_name': f"u/{post_data.get('author', 'Unknown')}",
                    'author_followers': 0,  # Reddit doesn't expose follower counts easily
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'timestamp': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                    'sentiment': sentiment,
                    'sentiment_score': score,
                    'likes': post_data.get('ups', 0),
                    'comments': comments,
                    'engagement': post_data.get('ups', 0) + comments,
                    'reach': subreddit_subscribers if subreddit_subscribers > 0 else karma * 10,  # Estimate reach
                    'subreddit': subreddit,
                    'subreddit_subscribers': subreddit_subscribers,
                    'awards': awards,
                    'upvote_ratio': post_data.get('upvote_ratio', 0),
                    'influence_score': round(influence_score, 2),
                    'source_quality': source_quality,
                    'content_type': 'post',
                    'is_video': post_data.get('is_video', False),
                    'domain': post_data.get('domain', 'self.reddit'),
                    'location': None  # Reddit doesn't provide location
                }
                mentions.append(mention)
            
            print(f"[OK] Found {len(mentions)} Reddit posts for '{keyword}'")
            return mentions
            
        except Exception as e:
            print(f"[ERROR] Reddit scraping error: {str(e)}")
            return []

if __name__ == "__main__":
    # Test the scraper
    scraper = RedditScraper()
    results = scraper.search_mentions("Nike", limit=10)
    
    for mention in results:
        print(f"\n[r/{mention['subreddit']}] {mention['text'][:80]}...")
        print(f"Author: u/{mention['author']}")
        print(f"Sentiment: {mention['sentiment']} ({mention['sentiment_score']:.2f})")
        print(f"Engagement: {mention['engagement']} (Likes:{mention['likes']} Comments:{mention['comments']})")
