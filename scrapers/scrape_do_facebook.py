"""
Facebook Scraper using Scrape.do - UNLIMITED scraping
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import os
from textblob import TextBlob
import re

class ScrapedoFacebookScraper:
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
        print(f"[INFO] Facebook (Scrape.do): Starting UNLIMITED scraping for '{keyword}'")
        
        mentions = []
        search_url = f"https://www.facebook.com/search/posts/?q={keyword}"
        
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
                posts = soup.find_all('div', {'data-ft': True})
                
                if not posts:
                    posts = soup.find_all('article')
                
                if not posts:
                    posts = soup.find_all('div', {'role': 'article'})
                
                print(f"[INFO] Facebook: Found {len(posts)} post elements")
                
                for post in posts:
                    if max_results and len(mentions) >= max_results:
                        break
                    
                    try:
                        text_elem = post.find('div', {'data-ad-comet-preview': 'message'})
                        if not text_elem:
                            text_elem = post
                        text = text_elem.get_text() if text_elem else ""
                        
                        if keyword.lower() not in text.lower():
                            continue
                        
                        author_elem = post.find('a', {'role': 'link'})
                        if not author_elem:
                            author_elem = post.find('strong')
                        author = author_elem.get_text() if author_elem else "unknown"
                        
                        url_elem = post.find('a', href=lambda x: x and ('/posts/' in x or '/permalink/' in x))
                        url = url_elem.get('href', '') if url_elem else ""
                        if url and not url.startswith('http'):
                            url = f"https://www.facebook.com{url}"
                        
                        mention = {
                            'platform': 'facebook',
                            'text': self.clean_text(text),
                            'url': url if url else "https://www.facebook.com",
                            'author': author,
                            'created_at': datetime.now(timezone.utc),
                            'sentiment': self.get_sentiment(text),
                            'engagement': {'likes': 0, 'shares': 0, 'comments': 0},
                            'metadata': {'scraped_with': 'scrape.do', 'unlimited': True}
                        }
                        
                        mentions.append(mention)
                        
                    except Exception as e:
                        print(f"[WARNING] Facebook: Error parsing - {str(e)}")
                        continue
                
                print(f"[OK] Facebook: Scraped {len(mentions)} mentions")
                
            else:
                print(f"[ERROR] Facebook: Scrape.do returned status {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Facebook scraping failed: {str(e)}")
        
        return mentions

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "test"
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    scraper = ScrapedoFacebookScraper()
    results = scraper.search_mentions(keyword, max_results)
    
    print(f"\n[SUMMARY] Facebook: Found {len(results)} mentions")
