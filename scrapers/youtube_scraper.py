"""
YouTube Scraper using Google API
Searches for videos and comments mentioning a specific keyword
"""
from googleapiclient.discovery import build
import os
from datetime import datetime, timedelta
from textblob import TextBlob

class YouTubeScraper:
    def __init__(self):
        # YouTube API key from environment
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        
        if self.api_key:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        else:
            self.youtube = None
            print("⚠️  YouTube API key not found. Please set YOUTUBE_API_KEY in .env")
    
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
    
    def search_mentions(self, keyword, max_results=50, days_back=7):
        """
        Search for YouTube videos mentioning the keyword
        
        Args:
            keyword: Search term
            max_results: Maximum videos to return (default 50, max 50 per request)
            days_back: How many days back to search
            
        Returns:
            List of mention dictionaries
        """
        if not self.youtube:
            return []
        
        try:
            # Calculate published_after date
            published_after = (datetime.utcnow() - timedelta(days=days_back)).isoformat() + 'Z'
            
            # Search videos
            search_response = self.youtube.search().list(
                q=keyword,
                part='snippet',
                maxResults=min(max_results, 50),
                publishedAfter=published_after,
                type='video',
                order='relevance'
            ).execute()
            
            mentions = []
            video_ids = []
            
            for item in search_response.get('items', []):
                video_ids.append(item['id']['videoId'])
            
            if not video_ids:
                return []
            
            # Get video statistics
            videos_response = self.youtube.videos().list(
                id=','.join(video_ids),
                part='statistics,snippet'
            ).execute()
            
            for video in videos_response.get('items', []):
                snippet = video['snippet']
                stats = video['statistics']
                sentiment, score = self.analyze_sentiment(snippet['title'] + ' ' + snippet.get('description', ''))
                
                mention = {
                    'platform': 'youtube',
                    'keyword': keyword,
                    'text': f"{snippet['title']}\n{snippet.get('description', '')[:200]}",
                    'author': snippet['channelTitle'],
                    'author_name': snippet['channelTitle'],
                    'author_followers': 0,  # Would need additional API call
                    'url': f"https://www.youtube.com/watch?v={video['id']}",
                    'timestamp': snippet['publishedAt'],
                    'sentiment': sentiment,
                    'sentiment_score': score,
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                    'engagement': int(stats.get('likeCount', 0)) + int(stats.get('commentCount', 0)),
                    'reach': int(stats.get('viewCount', 0))
                }
                mentions.append(mention)
            
            print(f"✅ Found {len(mentions)} YouTube videos for '{keyword}'")
            return mentions
            
        except Exception as e:
            print(f"❌ YouTube scraping error: {str(e)}")
            return []

if __name__ == "__main__":
    # Test the scraper
    from dotenv import load_dotenv
    load_dotenv('../.env')
    
    scraper = YouTubeScraper()
    results = scraper.search_mentions("Nike", max_results=10)
    
    for mention in results:
        print(f"\n{mention['author']}: {mention['text'][:100]}...")
        print(f"Sentiment: {mention['sentiment']} | Views: {mention['views']} | Likes: {mention['likes']}")
