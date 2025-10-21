from dotenv import load_dotenv
load_dotenv('../.env')
from youtube_scraper import YouTubeScraper

scraper = YouTubeScraper()
print("Testing YouTube search for 'StratSchool' with 365 days...")
results = scraper.search_mentions('StratSchool', max_results=20, days_back=365)
print(f"\nTotal results: {len(results)}")

for r in results[:10]:
    print(f"\n- {r['text']}")
    print(f"  Views: {r['views']} | Likes: {r['likes']} | Comments: {r['comments']}")
