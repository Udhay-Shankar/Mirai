"""
Master Scraper using Scrape.do - UNLIMITED scraping across ALL platforms
"""
import sys
import os
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

from scrape_do_twitter import ScrapedoTwitterScraper
from scrape_do_reddit import ScrapedoRedditScraper
from scrape_do_youtube import ScrapedoYouTubeScraper
from scrape_do_instagram import ScrapedoInstagramScraper
from scrape_do_facebook import ScrapedoFacebookScraper
from scrape_do_blogs import ScrapedoBlogScraper

load_dotenv()

def save_to_mongodb(mentions, keyword):
    try:
        mongodb_uri = os.getenv('MONGODB_URI')
        client = MongoClient(mongodb_uri)
        db = client['mirai_social_listening']
        collection = db['mentions']
        
        saved_count = 0
        updated_count = 0
        
        for mention in mentions:
            try:
                mention_doc = {
                    'keyword': keyword,
                    'keywords': [keyword],
                    'platform': mention['platform'],
                    'text': mention['text'],
                    'url': mention['url'],
                    'author': mention['author'],
                    'sentiment': mention['sentiment'],
                    'engagement': mention['engagement'],
                    'metadata': mention['metadata'],
                    'created_at': mention['created_at'],
                    'scraped_at': datetime.now(timezone.utc)
                }
                
                result = collection.update_one(
                    {'url': mention['url']},
                    {
                        '$set': mention_doc,
                        '$addToSet': {'keywords': keyword}
                    },
                    upsert=True
                )
                
                if result.upserted_id:
                    saved_count += 1
                elif result.modified_count > 0:
                    updated_count += 1
                    
            except Exception as e:
                print(f"[WARNING] MongoDB: Error saving mention - {str(e)}")
                continue
        
        print(f"[OK] MongoDB: Saved {saved_count} new, updated {updated_count} existing mentions")
        
        client.close()
        return saved_count + updated_count
        
    except Exception as e:
        print(f"[ERROR] MongoDB connection failed: {str(e)}")
        return 0

def main():
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python main_scraper_scrape_do.py <keyword> [max_per_platform]")
        sys.exit(1)
    
    keyword = sys.argv[1]
    max_per_platform = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    print("=" * 80)
    print(f"[INFO] Starting UNLIMITED scraping for keyword: '{keyword}'")
    if max_per_platform:
        print(f"[INFO] Max per platform: {max_per_platform}")
    else:
        print(f"[INFO] Max per platform: UNLIMITED (will scrape ALL available data)")
    print(f"[INFO] Using Scrape.do with rotating proxies - NO RATE LIMITS!")
    print("=" * 80)
    
    all_mentions = []
    
    twitter_scraper = ScrapedoTwitterScraper()
    reddit_scraper = ScrapedoRedditScraper()
    youtube_scraper = ScrapedoYouTubeScraper()
    instagram_scraper = ScrapedoInstagramScraper()
    facebook_scraper = ScrapedoFacebookScraper()
    blog_scraper = ScrapedoBlogScraper()
    
    print("\n" + "=" * 80)
    print("[INFO] Scraping Twitter...")
    print("=" * 80)
    try:
        twitter_mentions = twitter_scraper.search_mentions(keyword, max_per_platform)
        all_mentions.extend(twitter_mentions)
        print(f"[OK] Twitter: {len(twitter_mentions)} mentions collected")
    except Exception as e:
        print(f"[ERROR] Twitter: {str(e)}")
    
    print("\n" + "=" * 80)
    print("[INFO] Scraping Reddit...")
    print("=" * 80)
    try:
        reddit_mentions = reddit_scraper.search_mentions(keyword, max_per_platform)
        all_mentions.extend(reddit_mentions)
        print(f"[OK] Reddit: {len(reddit_mentions)} mentions collected")
    except Exception as e:
        print(f"[ERROR] Reddit: {str(e)}")
    
    print("\n" + "=" * 80)
    print("[INFO] Scraping YouTube...")
    print("=" * 80)
    try:
        youtube_mentions = youtube_scraper.search_mentions(keyword, max_per_platform)
        all_mentions.extend(youtube_mentions)
        print(f"[OK] YouTube: {len(youtube_mentions)} mentions collected")
    except Exception as e:
        print(f"[ERROR] YouTube: {str(e)}")
    
    print("\n" + "=" * 80)
    print("[INFO] Scraping Instagram...")
    print("=" * 80)
    try:
        instagram_mentions = instagram_scraper.search_mentions(keyword, max_per_platform)
        all_mentions.extend(instagram_mentions)
        print(f"[OK] Instagram: {len(instagram_mentions)} mentions collected")
    except Exception as e:
        print(f"[ERROR] Instagram: {str(e)}")
    
    print("\n" + "=" * 80)
    print("[INFO] Scraping Facebook...")
    print("=" * 80)
    try:
        facebook_mentions = facebook_scraper.search_mentions(keyword, max_per_platform)
        all_mentions.extend(facebook_mentions)
        print(f"[OK] Facebook: {len(facebook_mentions)} mentions collected")
    except Exception as e:
        print(f"[ERROR] Facebook: {str(e)}")
    
    print("\n" + "=" * 80)
    print("[INFO] Scraping Blogs...")
    print("=" * 80)
    try:
        blog_mentions = blog_scraper.search_mentions(keyword, max_per_platform)
        all_mentions.extend(blog_mentions)
        print(f"[OK] Blogs: {len(blog_mentions)} mentions collected")
    except Exception as e:
        print(f"[ERROR] Blogs: {str(e)}")
    
    print("\n" + "=" * 80)
    print("[INFO] Saving to MongoDB...")
    print("=" * 80)
    if all_mentions:
        saved = save_to_mongodb(all_mentions, keyword)
        print(f"[OK] Saved/updated {saved} mentions in MongoDB")
    else:
        print("[WARNING] No mentions to save")
    
    print("\n" + "=" * 80)
    print("[SUMMARY] Scraping completed!")
    print("=" * 80)
    print(f"Keyword: {keyword}")
    print(f"Total mentions collected: {len(all_mentions)}")
    print(f"Platform breakdown:")
    
    platforms = {}
    for mention in all_mentions:
        platform = mention['platform']
        platforms[platform] = platforms.get(platform, 0) + 1
    
    for platform, count in sorted(platforms.items()):
        print(f"  - {platform.capitalize()}: {count}")
    
    print("=" * 80)

if __name__ == '__main__':
    main()
