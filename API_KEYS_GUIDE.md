# 🔑 API Keys Setup Guide

This guide will help you get FREE API keys for all the social media platforms we scrape.

## 🐦 Twitter API (FREE - Essential Access)

### Step-by-Step:

1. **Create a Twitter Developer Account**
   - Go to: https://developer.twitter.com/
   - Click "Sign up" (use your Twitter account)
   - Complete the application form

2. **Create a New App**
   - Go to Developer Portal: https://developer.twitter.com/en/portal/dashboard
   - Click "Create App"
   - Enter app name (e.g., "Mirai Social Listening")
   - Note down your **API Key** and **API Secret**

3. **Generate Bearer Token**
   - In your app dashboard, go to "Keys and tokens"
   - Under "Authentication Tokens", click "Generate" for Bearer Token
   - **Copy this token immediately** - you can't see it again!

4. **Add to .env**
   ```
   TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAABcdefgh...
   ```

### Free Tier Limits:
- ✅ 500,000 tweets/month
- ✅ 10,000 requests/month
- ✅ Real-time search
- ⏱️ Rate limit: 450 requests per 15 minutes

---

## 🤖 Reddit API (100% FREE)

### Step-by-Step:

1. **Login to Reddit**
   - Go to: https://www.reddit.com/
   - Make sure you're logged in

2. **Create an App**
   - Go to: https://www.reddit.com/prefs/apps
   - Scroll to bottom, click "create another app"
   - Fill in:
     - **name**: Mirai Scraper
     - **type**: Choose "script"
     - **description**: Social listening tool
     - **about url**: leave blank
     - **redirect uri**: http://localhost:8080

3. **Copy Credentials**
   - After creating, you'll see:
     - **Client ID**: The string under "personal use script" (looks like: `abc123XYZ`)
     - **Client Secret**: The secret field (looks like: `xyz789ABC-def456`)

4. **Add to .env**
   ```
   REDDIT_CLIENT_ID=abc123XYZ
   REDDIT_CLIENT_SECRET=xyz789ABC-def456
   ```

### Free Tier Limits:
- ✅ Unlimited (within rate limits)
- ✅ ~60 requests per minute
- ✅ Access to all subreddits
- ✅ Full post history

---

## 🎥 YouTube Data API v3 (FREE)

### Step-by-Step:

1. **Create a Google Cloud Project**
   - Go to: https://console.developers.google.com/
   - Click "Select a project" → "New Project"
   - Enter project name: "Mirai Social Listening"
   - Click "Create"

2. **Enable YouTube Data API v3**
   - In the left sidebar, click "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click on it, then click "Enable"

3. **Create API Key**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - **Copy the API key immediately!**
   - (Optional) Click "Restrict Key" to limit usage to YouTube API only

4. **Add to .env**
   ```
   YOUTUBE_API_KEY=AIzaSyBcdefgh1234567890...
   ```

### Free Tier Limits:
- ✅ 10,000 units per day (free forever)
- ✅ 1 search = ~100 units = 100 searches/day
- ✅ Access to all public videos
- ✅ Comments, likes, views data

---

## 📝 Complete .env File Example

Open your `.env` file in the root directory and add:

```env
# MongoDB (Already configured)
MONGODB_URI=mongodb+srv://CFO-Login:qzJExUAezWWY87Z1@portfolio.blg8lko.mongodb.net/mirai_social_listening

# JWT Secret (Already configured)
JWT_SECRET=mirai_super_secret_jwt_key_2024

# Backend Port (Already configured)
PORT=8000

# Twitter API
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAABcdefgh_your_actual_bearer_token_here

# Reddit API
REDDIT_CLIENT_ID=abc123XYZ_your_client_id
REDDIT_CLIENT_SECRET=xyz789ABC_your_client_secret

# YouTube API
YOUTUBE_API_KEY=AIzaSyBcdefgh_your_api_key_here
```

---

## ✅ Testing Your Setup

### 1. Test Twitter:
```bash
cd scrapers
python -c "from twitter_scraper import TwitterScraper; s = TwitterScraper(); print(s.search_tweets('Nike', max_results=5))"
```

### 2. Test Reddit:
```bash
python -c "from reddit_scraper import RedditScraper; s = RedditScraper(); print(s.search_posts('Nike', limit=5))"
```

### 3. Test YouTube:
```bash
python -c "from youtube_scraper import YouTubeScraper; s = YouTubeScraper(); print(s.search_videos('Nike', max_results=5))"
```

### 4. Test Full System:
```bash
python main_scraper.py Nike
```

---

## 🚨 Troubleshooting

### Error: "401 Unauthorized" (Twitter)
- ❌ Bearer token is wrong
- ✅ Copy the EXACT token from Twitter Developer Portal
- ✅ Make sure there are NO spaces before or after

### Error: "Invalid credentials" (Reddit)
- ❌ Client ID or Secret is wrong
- ✅ Client ID is the string UNDER your app name (not the app name itself)
- ✅ Client Secret is the "secret" field

### Error: "API key not valid" (YouTube)
- ❌ API key is wrong or restricted
- ✅ Make sure YouTube Data API v3 is ENABLED
- ✅ Check if API key restrictions are too strict

### Error: "Quota exceeded" (YouTube)
- ❌ You've used 10,000 units today
- ✅ Wait until tomorrow (resets at midnight PST)
- ✅ Or create another Google Cloud project for more quota

---

## 💡 Pro Tips

1. **Never commit API keys to Git!**
   - `.env` is already in `.gitignore`
   - Use `.env.example` for templates

2. **Rate Limiting**
   - Our scrapers automatically handle rate limits
   - Twitter: Max 10 requests per minute
   - Reddit: Max 60 requests per minute
   - YouTube: Max 100 searches per day

3. **Cost Optimization**
   - All these APIs are FREE forever!
   - No credit card required
   - Perfect for building MVPs

4. **Upgrading Later**
   - Twitter: $100/month for v2 elevated
   - Reddit: Always free
   - YouTube: Always free (10k units/day)

---

## 🎉 You're Ready!

Once all API keys are set:
1. ✅ Start backend: `npm start` (in backend_node/)
2. ✅ Start frontend: `npm run dev` (in frontend/)
3. ✅ Search for keywords in dashboard
4. ✅ Watch the mentions roll in! 🚀

Happy listening! 🎧
