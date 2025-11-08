"""
Twitter Scraper using Scrape.do - UNLIMITED scraping with rotating proxies
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json
import os
from textblob import TextBlob
import re

class ScrapedoTwitterScraper:
    def __init__(self):
        self.api_key = os.getenv('SCRAPE_DO_API_KEY')
        self.base_url = "https://api.scrape.do"
        
    def clean_text(self, text):
        return ' '.join(text.split())
    
    def get_sentiment(self, text):
        try:
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity
            
            if polarity > 0.1:
                return 'positive'
            elif polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
        except:
            return 'neutral'
    
    def search_mentions(self, keyword, max_results=None):
        print(f"[INFO] Twitter (Scrape.do): Starting UNLIMITED scraping for '{keyword}'")
        
        mentions = []
        search_url = f"https://twitter.com/search?q={keyword}&src=typed_query&f=live"
        
        params = {
            'token': self.api_key,
            'url': search_url,
            'render': 'true',
            'country': 'us'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=60)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                tweets = soup.find_all('article', {'data-testid': 'tweet'})
                
                if not tweets:
                    tweets = soup.find_all('div', {'class': 'css-1dbjc4n'})
                
                print(f"[INFO] Twitter: Found {len(tweets)} tweet elements")
                
                for tweet in tweets:
                    if max_results and len(mentions) >= max_results:
                        break
                    
                    try:
                        text_elem = tweet.find('div', {'lang': True})
                        text = text_elem.get_text() if text_elem else ""
                        
                        if keyword.lower() not in text.lower():
                            continue
                        
                        username_elem = tweet.find('span', string=lambda x: x and x.startswith('@'))
                        username = username_elem.get_text() if username_elem else "unknown"
                        
                        mention = {
                            'platform': 'twitter',
                            'text': self.clean_text(text),
                            'url': f"https://twitter.com/{username.replace('@', '')}/status/",
                            'author': username,
                            'created_at': datetime.now(timezone.utc),
                            'sentiment': self.get_sentiment(text),
                            'engagement': {'likes': 0, 'retweets': 0, 'replies': 0},
                            'metadata': {'scraped_with': 'scrape.do', 'unlimited': True}
                        }
                        
                        mentions.append(mention)
                        
                    except Exception as e:
                        print(f"[WARNING] Twitter: Error parsing tweet - {str(e)}")
                        continue
                
                print(f"[OK] Twitter: Scraped {len(mentions)} mentions")
                
            else:
                print(f"[ERROR] Twitter: Scrape.do returned status {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Twitter scraping failed: {str(e)}")
        
        return mentions

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "test"
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    scraper = ScrapedoTwitterScraper()
    results = scraper.search_mentions(keyword, max_results)
    
    print(f"\n[SUMMARY] Twitter: Found {len(results)} mentions for '{keyword}'")
    for mention in results[:3]:
        print(f"  - {mention['author']}: {mention['text'][:100]}...")
