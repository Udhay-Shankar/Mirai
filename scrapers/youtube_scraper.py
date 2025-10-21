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
            print("[WARNING] YouTube API key not found. Please set YOUTUBE_API_KEY in .env")
    
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
        Search for YouTube videos mentioning the keyword with enhanced metadata
        
        Args:
            keyword: Search term (exact phrase if contains spaces)
            max_results: Maximum videos to return (default 50, max 50 per request)
            days_back: How many days back to search
            
        Returns:
            List of mention dictionaries with rich metadata
        """
        if not self.youtube:
            return []
        
        try:
            # Calculate published_after date
            published_after = (datetime.utcnow() - timedelta(days=days_back)).isoformat() + 'Z'
            
            # Enhance search query for better matching
            if ' ' in keyword or len(keyword.split()) > 1:
                search_query = f'"{keyword}"'  # Exact phrase
            else:
                search_query = keyword
            
            # Search videos
            search_response = self.youtube.search().list(
                q=search_query,
                part='snippet',
                maxResults=min(max_results, 50),
                publishedAfter=published_after,
                type='video',
                order='relevance',
                relevanceLanguage='en'
            ).execute()
            
            mentions = []
            video_ids = []
            
            for item in search_response.get('items', []):
                video_ids.append(item['id']['videoId'])
            
            if not video_ids:
                return []
            
            # Get video statistics and channel details
            videos_response = self.youtube.videos().list(
                id=','.join(video_ids),
                part='statistics,snippet,contentDetails'
            ).execute()
            
            # Get channel statistics for all unique channels
            channel_ids = list(set([v['snippet']['channelId'] for v in videos_response.get('items', [])]))
            channels_response = self.youtube.channels().list(
                id=','.join(channel_ids),
                part='statistics,snippet'
            ).execute()
            
            # Create channel lookup
            channels = {c['id']: c for c in channels_response.get('items', [])}
            
            for video in videos_response.get('items', []):
                snippet = video['snippet']
                stats = video['statistics']
                channel_id = snippet['channelId']
                channel = channels.get(channel_id, {})
                channel_stats = channel.get('statistics', {})
                
                # Additional filtering - check if keyword appears in title or description
                title_lower = snippet['title'].lower()
                desc_lower = snippet.get('description', '').lower()
                keyword_lower = keyword.lower()
                
                if ' ' in keyword:
                    if keyword_lower not in title_lower and keyword_lower not in desc_lower:
                        continue
                
                sentiment, score = self.analyze_sentiment(snippet['title'] + ' ' + snippet.get('description', ''))
                
                # Extract tags
                tags = snippet.get('tags', [])
                
                # Calculate metrics
                views = int(stats.get('viewCount', 0))
                likes = int(stats.get('likeCount', 0))
                comments_count = int(stats.get('commentCount', 0))
                subscribers = int(channel_stats.get('subscriberCount', 0))
                
                # Calculate influence score
                engagement_rate = (likes + comments_count) / max(views, 1) * 100
                influence_score = min(100, (subscribers / 100000) * 50 + engagement_rate * 50)
                
                # Determine source quality
                source_quality = 'high' if subscribers > 100000 else ('medium' if subscribers > 10000 else 'low')
                
                # Get video duration
                duration = video.get('contentDetails', {}).get('duration', 'PT0S')
                
                mention = {
                    'platform': 'youtube',
                    'keyword': keyword,
                    'text': snippet['title'],
                    'full_text': f"{snippet['title']}\n{snippet.get('description', '')[:300]}",
                    'author': snippet['channelTitle'],
                    'author_name': snippet['channelTitle'],
                    'author_followers': subscribers,
                    'author_verified': False,  # YouTube API doesn't easily expose verified status
                    'channel_id': channel_id,
                    'url': f"https://www.youtube.com/watch?v={video['id']}",
                    'timestamp': snippet['publishedAt'],
                    'sentiment': sentiment,
                    'sentiment_score': score,
                    'views': views,
                    'likes': likes,
                    'comments': comments_count,
                    'engagement': likes + comments_count,
                    'reach': views + (subscribers // 10),  # Views + % of subscriber base
                    'tags': tags[:10],  # Top 10 tags
                    'duration': duration,
                    'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    'channel_subscribers': subscribers,
                    'engagement_rate': round(engagement_rate, 2),
                    'influence_score': round(influence_score, 2),
                    'source_quality': source_quality,
                    'content_type': 'video',
                    'location': None  # Would need additional API calls
                }
                mentions.append(mention)
            
            print(f"[OK] Found {len(mentions)} YouTube videos for '{keyword}'")
            return mentions
            
        except Exception as e:
            print(f"[ERROR] YouTube scraping error: {str(e)}")
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
