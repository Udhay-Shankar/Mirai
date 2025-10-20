# 🎯 MIRAI - Complete Setup Guide
## Social Listening Platform (Awario Wrapper)

---

## 📌 WHAT IS MIRAI?

Mirai is a **social listening platform** that uses the Awario API to track mentions of keywords/brands across:
- Twitter/X
- Facebook
- Instagram
- YouTube
- Reddit
- News sites
- Blogs
- Forums

**Just like Awario**, it shows you:
- ✅ Where your keyword is mentioned
- ✅ Sentiment analysis (positive/negative/neutral)
- ✅ Influencers talking about it
- ✅ Trending hashtags and topics
- ✅ Reach and engagement metrics
- ✅ Time-based trends

---

## 🔑 WHAT YOU NEED

### 1. **Awario API Key** (MOST IMPORTANT!)

**Without this, the app won't work at all.**

**How to get:**
1. Visit: https://awario.com/
2. Click "Start Free Trial" or "Sign Up"
3. Create an account
4. Go to **Settings** → **API** in your Awario dashboard
5. Click "Generate API Key"
6. Copy the API key (looks like: `awario_1234567890abcdef...`)

**Pricing:**
- ✅ Free Trial: 7-14 days (perfect for testing)
- Starter: $29/month (5 alerts, 30K mentions/month)
- Pro: $89/month (15 alerts, 150K mentions/month)
- Enterprise: Custom pricing

⚠️ **NOTE:** The free trial is enough to test your app!

---

### 2. **Firebase Account** (For User Authentication)

**Free forever for small projects!**

**Setup Steps:**

#### A. Create Firebase Project:
1. Go to: https://console.firebase.google.com/
2. Click "Add Project"
3. Enter project name (e.g., "Mirai-App")
4. Disable Google Analytics (not needed)
5. Click "Create Project"

#### B. Enable Authentication:
1. In Firebase Console, click "Authentication"
2. Click "Get Started"
3. Enable these sign-in methods:
   - **Email/Password** (click, then toggle "Enable")
   - **Google** (click, enter project name, your email)
   - Facebook (optional)
   - Phone (optional)

#### C. Get Firebase Admin Credentials (for Backend):
1. Click the gear icon ⚙️ → "Project Settings"
2. Go to "Service Accounts" tab
3. Click "Generate New Private Key"
4. Download the JSON file
5. Save it as `firebase-credentials.json` in `backend/` folder

#### D. Get Firebase Config (for Frontend):
1. In Project Settings, scroll down to "Your apps"
2. Click the web icon `</>`
3. Register app (name: "Mirai Web")
4. Copy the `firebaseConfig` object (you'll need these values)

---

## 🛠️ STEP-BY-STEP SETUP

### STEP 1: Backend Setup

1. **Navigate to backend folder:**
```powershell
cd "c:\Users\gokul\OneDrive\Desktop\mirai\Mirai\backend"
```

2. **Create virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

4. **Create `.env` file:**
```powershell
Copy-Item .env.example .env
```

5. **Edit `.env` file** (use Notepad or VS Code):
```bash
# Replace these with YOUR actual values:

AWARIO_API_KEY=your_awario_api_key_from_step_1

FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

JWT_SECRET_KEY=create_a_random_32_character_secret_key_here_abc123xyz

DATABASE_URL=sqlite:///./mirai.db

CORS_ORIGINS=http://localhost:5173,http://localhost:3000

DEBUG_MODE=True
RATE_LIMIT_PER_MINUTE=60
```

6. **Place Firebase JSON file:**
- Move the downloaded `firebase-credentials.json` to the `backend/` folder

7. **Start the backend:**
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Backend should now be running at:** http://localhost:8000
✅ **API Docs available at:** http://localhost:8000/docs

---

### STEP 2: Frontend Setup

1. **Open NEW terminal** (keep backend running)

2. **Navigate to frontend:**
```powershell
cd "c:\Users\gokul\OneDrive\Desktop\mirai\Mirai\frontend"
```

3. **Dependencies already installed** ✅ (you did this earlier)

4. **Create `.env` file:**
```powershell
Copy-Item .env.example .env
```

5. **Edit `.env` file** with Firebase config from earlier:
```bash
# Replace with YOUR Firebase config values:

VITE_FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abcdefghijk

VITE_API_BASE_URL=http://localhost:8000
```

6. **Start frontend:**
```powershell
npm run dev
```

✅ **Frontend should now be running at:** http://localhost:5173

---

## 🎉 TESTING THE APP

### 1. **Sign Up / Login**
1. Open http://localhost:5173
2. Click "Sign Up"
3. Register with email/password or Google
4. You should be redirected to the dashboard

### 2. **Search for Mentions**
1. In the dashboard, enter a keyword (e.g., "Nike", "Tesla", "iPhone")
2. Click "Search" or press Enter
3. Wait a few seconds...

**What you should see:**
- Total mentions count
- Sentiment breakdown (positive/negative/neutral)
- Top keywords/hashtags
- Source breakdown (Twitter, Facebook, etc.)
- Timeline chart (if premium)

### 3. **Test Free vs Premium Features**

**FREE TIER shows:**
- ✅ Total mention count
- ✅ Basic sentiment percentages
- ✅ Top 5 keywords
- ✅ Last 7 days data only
- ❌ No influencer list
- ❌ No detailed charts
- ❌ No competitor analysis

**PREMIUM TIER shows:**
- ✅ Everything from free
- ✅ Full influencer list
- ✅ Detailed time-series charts
- ✅ 30+ days historical data
- ✅ Demographic breakdown
- ✅ Competitor comparison
- ✅ Export functionality

---

## 🔧 TROUBLESHOOTING

### Problem: "Awario API authentication failed"
**Solution:**
- Check your `AWARIO_API_KEY` in `backend/.env`
- Make sure you copied the full key from Awario
- Verify your Awario subscription is active

### Problem: "Firebase authentication error"
**Solution:**
- Verify `firebase-credentials.json` exists in `backend/` folder
- Check all Firebase config values in `frontend/.env`
- Ensure authentication methods are enabled in Firebase Console

### Problem: "CORS error" in browser console
**Solution:**
- Make sure backend is running on port 8000
- Check `CORS_ORIGINS` in `backend/.env` includes `http://localhost:5173`

### Problem: "No mentions found"
**Solution:**
- Try a popular keyword first (e.g., "Apple", "Nike", "Tesla")
- Some keywords may have no recent mentions
- Check if your Awario subscription has available alerts/quota

### Problem: Backend won't start
**Solution:**
```powershell
# Make sure you're in the backend folder
cd "c:\Users\gokul\OneDrive\Desktop\mirai\Mirai\backend"

# Activate virtual environment
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Try starting again
uvicorn app.main:app --reload
```

---

## 📊 HOW IT WORKS (Technical Overview)

```
┌─────────────┐
│   User      │
│  Browser    │
└──────┬──────┘
       │
       │ 1. Search "Nike"
       ▼
┌─────────────────┐
│  React Frontend │  (http://localhost:5173)
│  (Mirai UI)     │
└────────┬────────┘
         │
         │ 2. POST /api/analytics/search
         ▼
┌──────────────────┐
│  FastAPI Backend │  (http://localhost:8000)
│  (Your Server)   │
└────────┬─────────┘
         │
         │ 3. Calls Awario API
         ▼
┌──────────────────┐
│   Awario API     │  (awario.com)
│  (Web Scraping)  │  - Scrapes Twitter, Facebook, etc.
└────────┬─────────┘  - Returns mentions data
         │
         │ 4. Returns data (JSON)
         ▼
┌──────────────────┐
│  Your Backend    │  - Processes data
│                  │  - Applies free/premium logic
└────────┬─────────┘  - Calculates analytics
         │
         │ 5. Sends formatted data
         ▼
┌──────────────────┐
│  Your Frontend   │  - Displays charts
│                  │  - Shows mentions
└──────────────────┘  - Renders dashboard
```

---

## 🎨 WHAT MIRAI DOES (User Perspective)

Imagine you're a brand manager for **"StratSchool"** (like in your screenshot):

1. **You enter "StratSchool"** in the search box
2. **Mirai asks Awario:** "Find all mentions of StratSchool across the internet"
3. **Awario scrapes:**
   - Twitter: StratSchool tweets
   - Facebook: Posts mentioning StratSchool
   - Instagram: #StratSchool posts
   - YouTube: Videos about StratSchool
   - Reddit: StratSchool discussions
   - News sites: Articles mentioning StratSchool
   - Blogs: Blog posts about StratSchool

4. **Mirai shows you:**
   - 📊 Total mentions: 184 reach
   - 😊 Sentiment: 70% positive, 20% neutral, 10% negative
   - 🔥 Trending topics: "startup", "IGNITE", "college"
   - 👥 Top influencers: People with most followers talking about it
   - 📈 Timeline: When mentions spiked
   - 🌍 Location: Where mentions are coming from

---

## 💡 ADVANCED FEATURES TO BUILD

Since you now have the base app working, here are features you can add:

### 1. **Email Alerts**
- Send daily/weekly digest emails
- Alert when mentions spike
- Notify on negative sentiment

### 2. **Competitor Tracking**
- Compare multiple keywords
- Share of voice analysis
- Side-by-side comparison

### 3. **Custom Dashboards**
- Save favorite keywords
- Create custom reports
- Schedule automated reports

### 4. **Advanced Filters**
- Filter by language
- Filter by location
- Filter by date range
- Filter by platform

### 5. **Export Features**
- Export to CSV
- Export to PDF reports
- Export to Excel

---

## 🚀 NEXT STEPS

1. ✅ Get Awario API key (free trial)
2. ✅ Set up Firebase project
3. ✅ Configure backend `.env`
4. ✅ Configure frontend `.env`
5. ✅ Start both servers
6. ✅ Test with a popular keyword
7. 🎉 Customize and deploy!

---

## 📞 NEED HELP?

If you run into issues:
1. Check the logs in both terminals
2. Verify all API keys are correct
3. Make sure ports 8000 and 5173 are not in use
4. Read the error messages carefully

**Common errors and solutions are in the TROUBLESHOOTING section above.**

---

## 🎊 HAPPY DIWALI! 

Your app is ready to track mentions during the festive season! 🪔

Start by searching for "Diwali" and see what people are saying! ✨
