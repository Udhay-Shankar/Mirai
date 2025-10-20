# 🔍 Mirai Scrapers - Social Listening Platform

Professional-grade web scrapers for tracking brand mentions across social media.

## 📦 What's Included

- **Twitter Scraper** - Using Twitter API v2
- **Reddit Scraper** - Using PRAW (Reddit API)
- **YouTube Scraper** - Using YouTube Data API v3
- **Sentiment Analysis** - Using TextBlob
- **MongoDB Integration** - Auto-saves all mentions

## 🚀 Quick Setup

### 1. Install Python Dependencies

```bash
cd scrapers
pip install -r requirements.txt
```

Or create a virtual environment (recommended):
```bash
cd scrapers
python -m venv venv
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2. Get API Keys

#### Twitter API (Free)
1. Go to https://developer.twitter.com/
2. Create a new app
3. Generate Bearer Token
4. Add to `.env`: `TWITTER_BEARER_TOKEN=your_token`

#### Reddit API (Free)
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" → choose "script"
3. Copy Client ID and Secret
4. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_secret
   ```

#### YouTube API (Free - 10,000 units/day)
1. Go to https://console.developers.google.com/
2. Create a project
3. Enable "YouTube Data API v3"
4. Create credentials → API Key
5. Add to `.env`: `YOUTUBE_API_KEY=your_key`

### 3. Test Individual Scrapers

```bash
# Test Twitter
python twitter_scraper.py

# Test Reddit
python reddit_scraper.py

# Test YouTube
python youtube_scraper.py
```

### 4. Run Full Scraper

```bash
# Scrape all platforms for a keyword
python main_scraper.py Nike

# Or
python main_scraper.py "Tesla"
```

## 📊 How It Works

```
User types keyword in dashboard
         ↓
Frontend calls: POST /api/scrape/search
         ↓
Node backend triggers: main_scraper.py
         ↓
Python scrapers run in parallel:
  - Twitter API → Tweets
  - Reddit API → Posts
  - YouTube API → Videos
         ↓
Sentiment analysis on each mention
         ↓
Save to MongoDB (mentions collection)
         ↓
Frontend fetches: GET /api/scrape/mentions/:keyword
         ↓
Display in dashboard with charts!
```

## 🎯 Data Structure

Each mention saved to MongoDB:

```json
{
  "platform": "twitter",
  "keyword": "Nike",
  "text": "Just bought new Nike shoes!",
  "author": "john_doe",
  "url": "https://twitter.com/john_doe/status/123",
  "timestamp": "2025-10-20T12:00:00Z",
  "sentiment": "positive",
  "sentiment_score": 0.75,
  "likes": 150,
  "retweets": 30,
  "engagement": 180,
  "reach": 5000,
  "scraped_at": "2025-10-20T12:05:00Z"
}
```

## 🔧 Configuration

All API keys are in the root `.env` file:

```env
# Twitter
TWITTER_BEARER_TOKEN=your_bearer_token

# Reddit
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret

# YouTube
YOUTUBE_API_KEY=your_api_key

# MongoDB (already configured)
MONGODB_URI=mongodb+srv://...
```

## 📈 API Rate Limits

- **Twitter**: 450 requests / 15 min (Free tier)
- **Reddit**: ~60 requests / minute (varies)
- **YouTube**: 10,000 units/day (1 search = ~100 units)

## 🎨 Frontend Integration

The dashboard will automatically:
1. Call backend API when user searches
2. Display loading state
3. Show results with charts:
   - Total mentions
   - Platform breakdown
   - Sentiment analysis
   - Top influencers
   - Timeline chart

## 🐛 Troubleshooting

**"No module named 'tweepy'"**
- Run: `pip install -r requirements.txt`

**"Twitter API credentials not found"**
- Add `TWITTER_BEARER_TOKEN` to `.env`

**"Failed to connect to MongoDB"**
- Check `MONGODB_URI` in `.env`

## 🎉 Next Steps

Once scrapers are working:
1. ✅ Get API keys
2. ✅ Test scrapers individually  
3. ✅ Run full scraper
4. ✅ Check MongoDB for data
5. ✅ Frontend will display automatically!

Happy scraping! 🚀
