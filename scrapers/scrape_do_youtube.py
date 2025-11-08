"""
YouTube Scraper using Scrape.do - UNLIMITED scraping
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json
import os
from textblob import TextBlob
import re

class ScrapedoYouTubeScraper:
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
        print(f"[INFO] YouTube (Scrape.do): Starting UNLIMITED scraping for '{keyword}'")
        
        mentions = []
        search_url = f"https://www.youtube.com/results?search_query={keyword}"
        
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
                scripts = soup.find_all('script')
                yt_data = None
                
                for script in scripts:
                    if 'var ytInitialData' in script.text:
                        json_text = script.text.split('var ytInitialData = ')[1].split(';</script>')[0]
                        try:
                            yt_data = json.loads(json_text)
                            break
                        except:
                            continue
                
                if yt_data:
                    try:
                        contents = yt_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
                        
                        for item in contents:
                            if max_results and len(mentions) >= max_results:
                                break
                            
                            if 'videoRenderer' not in item:
                                continue
                            
                            video = item['videoRenderer']
                            video_id = video.get('videoId', '')
                            title = video.get('title', {}).get('runs', [{}])[0].get('text', '')
                            description = video.get('descriptionSnippet', {}).get('runs', [{}])[0].get('text', '') if 'descriptionSnippet' in video else ''
                            
                            text = f"{title} {description}"
                            
                            if keyword.lower() not in text.lower():
                                continue
                            
                            channel = video.get('ownerText', {}).get('runs', [{}])[0].get('text', 'Unknown')
                            view_text = video.get('viewCountText', {}).get('simpleText', '0 views')
                            views = int(re.sub(r'[^\d]', '', view_text.split(' ')[0])) if view_text else 0
                            
                            mention = {
                                'platform': 'youtube',
                                'text': self.clean_text(text),
                                'url': f"https://www.youtube.com/watch?v={video_id}",
                                'author': channel,
                                'created_at': datetime.now(timezone.utc),
                                'sentiment': self.get_sentiment(text),
                                'engagement': {'views': views},
                                'metadata': {'video_id': video_id, 'scraped_with': 'scrape.do', 'unlimited': True}
                            }
                            
                            mentions.append(mention)
                            
                    except Exception as e:
                        print(f"[WARNING] YouTube: Error parsing ytInitialData - {str(e)}")
                
                print(f"[OK] YouTube: Scraped {len(mentions)} mentions")
                
            else:
                print(f"[ERROR] YouTube: Scrape.do returned status {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] YouTube scraping failed: {str(e)}")
        
        return mentions

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "test"
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    scraper = ScrapedoYouTubeScraper()
    results = scraper.search_mentions(keyword, max_results)
    
    print(f"\n[SUMMARY] YouTube: Found {len(results)} mentions for '{keyword}'")
