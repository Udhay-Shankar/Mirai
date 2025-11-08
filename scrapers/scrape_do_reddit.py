"""
Reddit Scraper using Scrape.do - UNLIMITED scraping with rotating proxies
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json
import os
from textblob import TextBlob
import re

class ScrapedoRedditScraper:
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
        print(f"[INFO] Reddit (Scrape.do): Starting UNLIMITED scraping for '{keyword}'")
        
        mentions = []
        search_url = f"https://www.reddit.com/search/?q={keyword}&sort=new"
        
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
                posts = soup.find_all(['div'], {'data-testid': lambda x: x and 'post-container' in x})
                
                if not posts:
                    posts = soup.find_all('div', {'class': lambda x: x and 'thing' in x})
                
                print(f"[INFO] Reddit: Found {len(posts)} post elements")
                
                for post in posts:
                    if max_results and len(mentions) >= max_results:
                        break
                    
                    try:
                        title_elem = post.find(['h3', 'a'], {'data-testid': 'post-title'})
                        if not title_elem:
                            title_elem = post.find('a', {'class': 'title'})
                        title = title_elem.get_text() if title_elem else ""
                        
                        body_elem = post.find('div', {'data-testid': 'post-content'})
                        body = body_elem.get_text() if body_elem else ""
                        text = f"{title} {body}"
                        
                        if keyword.lower() not in text.lower():
                            continue
                        
                        subreddit_elem = post.find('a', {'data-testid': 'subreddit-name'})
                        if not subreddit_elem:
                            subreddit_elem = post.find('a', {'class': 'subreddit'})
                        subreddit = subreddit_elem.get_text() if subreddit_elem else "unknown"
                        
                        author_elem = post.find('a', {'data-testid': 'post-author'})
                        if not author_elem:
                            author_elem = post.find('a', {'class': 'author'})
                        author = author_elem.get_text() if author_elem else "unknown"
                        
                        url_elem = post.find('a', {'data-click-id': 'comments'})
                        if not url_elem:
                            url_elem = title_elem
                        url = url_elem.get('href', '') if url_elem else ""
                        if url and not url.startswith('http'):
                            url = f"https://www.reddit.com{url}"
                        
                        mention = {
                            'platform': 'reddit',
                            'text': self.clean_text(text),
                            'url': url,
                            'author': f"u/{author}",
                            'created_at': datetime.now(timezone.utc),
                            'sentiment': self.get_sentiment(text),
                            'engagement': {'score': 0, 'comments': 0},
                            'metadata': {'subreddit': subreddit, 'scraped_with': 'scrape.do', 'unlimited': True}
                        }
                        
                        mentions.append(mention)
                        
                    except Exception as e:
                        print(f"[WARNING] Reddit: Error parsing post - {str(e)}")
                        continue
                
                print(f"[OK] Reddit: Scraped {len(mentions)} mentions")
                
            else:
                print(f"[ERROR] Reddit: Scrape.do returned status {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Reddit scraping failed: {str(e)}")
        
        return mentions

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "test"
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    scraper = ScrapedoRedditScraper()
    results = scraper.search_mentions(keyword, max_results)
    
    print(f"\n[SUMMARY] Reddit: Found {len(results)} mentions for '{keyword}'")
    for mention in results[:3]:
        print(f"  - {mention['author']} in {mention['metadata']['subreddit']}: {mention['text'][:100]}...")
