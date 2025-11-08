"""
Instagram Scraper using Scrape.do - UNLIMITED scraping
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json
import os
from textblob import TextBlob

class ScrapedoInstagramScraper:
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
        print(f"[INFO] Instagram (Scrape.do): Starting UNLIMITED scraping for '{keyword}'")
        
        mentions = []
        hashtag = keyword.replace(' ', '').replace('#', '')
        search_url = f"https://www.instagram.com/explore/tags/{hashtag}/"
        
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
                scripts = soup.find_all('script', type='text/javascript')
                ig_data = None
                
                for script in scripts:
                    if 'window._sharedData' in script.text:
                        json_text = script.text.split('window._sharedData = ')[1].split(';</script>')[0]
                        try:
                            ig_data = json.loads(json_text)
                            break
                        except:
                            continue
                
                if ig_data:
                    try:
                        tag_page = ig_data.get('entry_data', {}).get('TagPage', [{}])[0]
                        edges = tag_page.get('graphql', {}).get('hashtag', {}).get('edge_hashtag_to_media', {}).get('edges', [])
                        
                        for edge in edges:
                            if max_results and len(mentions) >= max_results:
                                break
                            
                            node = edge.get('node', {})
                            shortcode = node.get('shortcode', '')
                            caption_edges = node.get('edge_media_to_caption', {}).get('edges', [])
                            caption = caption_edges[0].get('node', {}).get('text', '') if caption_edges else ''
                            owner_username = node.get('owner', {}).get('username', 'unknown')
                            likes = node.get('edge_liked_by', {}).get('count', 0)
                            comments = node.get('edge_media_to_comment', {}).get('count', 0)
                            
                            mention = {
                                'platform': 'instagram',
                                'text': self.clean_text(caption) if caption else f"Post with #{hashtag}",
                                'url': f"https://www.instagram.com/p/{shortcode}/",
                                'author': f"@{owner_username}",
                                'created_at': datetime.now(timezone.utc),
                                'sentiment': self.get_sentiment(caption) if caption else 'neutral',
                                'engagement': {'likes': likes, 'comments': comments},
                                'metadata': {'hashtag': f"#{hashtag}", 'scraped_with': 'scrape.do', 'unlimited': True}
                            }
                            
                            mentions.append(mention)
                            
                    except Exception as e:
                        print(f"[WARNING] Instagram: Error parsing - {str(e)}")
                
                print(f"[OK] Instagram: Scraped {len(mentions)} mentions")
                
            else:
                print(f"[ERROR] Instagram: Scrape.do returned status {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Instagram scraping failed: {str(e)}")
        
        return mentions

if __name__ == '__main__':
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "test"
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    scraper = ScrapedoInstagramScraper()
    results = scraper.search_mentions(keyword, max_results)
    
    print(f"\n[SUMMARY] Instagram: Found {len(results)} mentions")
