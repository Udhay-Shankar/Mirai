"""
Main Scraper Orchestrator
Combines all scrapers and sends results to MongoDB
"""
import sys
import os
import json
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from twitter_scraper import TwitterScraper
from reddit_scraper import RedditScraper
from youtube_scraper import YouTubeScraper

class MiraiScraper:
    def __init__(self):
        # Load environment variables
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
        
        # Initialize MongoDB
        mongo_uri = os.getenv('MONGODB_URI')
        if mongo_uri:
            self.client = MongoClient(mongo_uri)
            db_name = mongo_uri.split('/')[-1].split('?')[0] if '/' in mongo_uri else 'mirai_social_listening'
            self.db = self.client[db_name]
            self.mentions_collection = self.db['mentions']
            print(f"[OK] Connected to MongoDB: {db_name}")
        else:
            self.client = None
            self.db = None
            print("[WARNING] MongoDB URI not found")
        
        # Initialize scrapers
        self.twitter = TwitterScraper()
        self.reddit = RedditScraper()
        self.youtube = YouTubeScraper()
    
    def scrape_all(self, keyword, max_per_platform=50):
        """
        Scrape all platforms for a keyword
        
        Args:
            keyword: Search term
            max_per_platform: Max results per platform
            
        Returns:
            Dictionary with results from all platforms
        """
        print(f"\n[INFO] Starting scraping for '{keyword}'...")
        
        all_mentions = []
        
        # Twitter
        print("\n[TWITTER] Scraping Twitter...")
        twitter_mentions = self.twitter.search_mentions(keyword, max_results=max_per_platform)
        all_mentions.extend(twitter_mentions)
        
        # Reddit
        print("\n[REDDIT] Scraping Reddit...")
        reddit_mentions = self.reddit.search_mentions(keyword, limit=max_per_platform)
        all_mentions.extend(reddit_mentions)
        
        # YouTube
        print("\n[YOUTUBE] Scraping YouTube...")
        youtube_mentions = self.youtube.search_mentions(keyword, max_results=max_per_platform, days_back=90)
        all_mentions.extend(youtube_mentions)
        
        # Save to MongoDB
        if self.db is not None and all_mentions:
            print(f"\n[MONGODB] Saving {len(all_mentions)} mentions to MongoDB...")
            for mention in all_mentions:
                mention['scraped_at'] = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
                # Update or insert
                self.mentions_collection.update_one(
                    {'url': mention['url'], 'keyword': keyword},
                    {'$set': mention},
                    upsert=True
                )
        
        # Aggregate results
        results = {
            'keyword': keyword,
            'total_mentions': len(all_mentions),
            'by_platform': {
                'twitter': len(twitter_mentions),
                'reddit': len(reddit_mentions),
                'youtube': len(youtube_mentions)
            },
            'sentiment': {
                'positive': len([m for m in all_mentions if m['sentiment'] == 'positive']),
                'negative': len([m for m in all_mentions if m['sentiment'] == 'negative']),
                'neutral': len([m for m in all_mentions if m['sentiment'] == 'neutral'])
            },
            'mentions': all_mentions
        }
        
        print(f"\n[OK] Scraping complete!")
        print(f"   Total: {results['total_mentions']}")
        print(f"   Twitter: {results['by_platform']['twitter']}")
        print(f"   Reddit: {results['by_platform']['reddit']}")
        print(f"   YouTube: {results['by_platform']['youtube']}")
        print(f"   Sentiment: +{results['sentiment']['positive']} ={results['sentiment']['neutral']} -{results['sentiment']['negative']}")
        
        return results

if __name__ == "__main__":
    # Test the orchestrator
    scraper = MiraiScraper()
    
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = "Nike"
    
    results = scraper.scrape_all(keyword, max_per_platform=10)
    
    # Print sample mentions
    print(f"\n[SAMPLE] Sample mentions:")
    for mention in results['mentions'][:5]:
        try:
            print(f"\n{mention['platform'].upper()}: {mention['author']}")
            print(f"   {mention['text'][:100]}...")
            print(f"   Sentiment: {mention['sentiment']} | Engagement: {mention.get('engagement', 0)}")
        except UnicodeEncodeError:
            print(f"\n{mention['platform'].upper()}: {mention['author']}")
            print(f"   [Text contains special characters]")
            print(f"   Sentiment: {mention['sentiment']} | Engagement: {mention.get('engagement', 0)}")
