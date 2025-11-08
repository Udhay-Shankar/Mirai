"""
Blog/Medium/Substack Scraper using Scrape.do - UNLIMITED scraping
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import os
from textblob import TextBlob

class ScrapedoBlogScraper:
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
    
    def scrape_google_blogs(self, keyword, max_results=None):
        print(f"[INFO] Blogs (Google): Searching for '{keyword}'")
        
        mentions = []
        search_url = f"https://www.google.com/search?q={keyword}+blog"
        
        params = {
            'token': self.api_key,
            'url': search_url,
            'render': 'false',
            'country': 'us'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=60)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('div', {'class': 'g'})
                
                for result in results:
                    if max_results and len(mentions) >= max_results:
                        break
                    
                    try:
                        title_elem = result.find('h3')
                        title = title_elem.get_text() if title_elem else ""
                        
                        link_elem = result.find('a')
                        url = link_elem.get('href', '') if link_elem else ""
                        
                        snippet_elem = result.find('div', {'class': lambda x: x and 'VwiC3b' in x})
                        if not snippet_elem:
                            snippet_elem = result.find('span', {'class': 'st'})
                        snippet = snippet_elem.get_text() if snippet_elem else ""
                        
                        text = f"{title} {snippet}"
                        
                        platform = 'blog'
                        if 'medium.com' in url:
                            platform = 'medium'
                        elif 'substack.com' in url:
                            platform = 'substack'
                        
                        mention = {
                            'platform': platform,
                            'text': self.clean_text(text),
                            'url': url,
                            'author': 'Blog Author',
                            'created_at': datetime.now(timezone.utc),
                            'sentiment': self.get_sentiment(text),
                            'engagement': {},
                            'metadata': {'source': 'google_search', 'scraped_with': 'scrape.do', 'unlimited': True}
                        }
                        
                        mentions.append(mention)
                        
                    except Exception as e:
                        print(f"[WARNING] Google: Error parsing - {str(e)}")
                        continue
                
            else:
                print(f"[ERROR] Google: Scrape.do returned status {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Google scraping failed: {str(e)}")
        
        return mentions
    
    def search_mentions(self, keyword, max_results=None):
        print(f"[INFO] Blogs (Scrape.do): Starting UNLIMITED scraping for '{keyword}'")
        
        all_mentions = []
        google_mentions = self.scrape_google_blogs(keyword, max_results)
        all_mentions.extend(google_mentions)
        
        print(f"[OK] Blogs (Total): Scraped {len(all_mentions)} mentions")
        
        return all_mentions

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "test"
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    scraper = ScrapedoBlogScraper()
    results = scraper.search_mentions(keyword, max_results)
    
    print(f"\n[SUMMARY] Blogs: Found {len(results)} mentions")
