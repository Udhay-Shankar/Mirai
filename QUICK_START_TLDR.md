# 🎯 MIRAI - Quick Start (TL;DR)

## What You Need (Just 2 Things!)

### 1. ⚡ Awario API Key
- Go to: https://awario.com/
- Sign up → Start FREE trial
- Settings → API → Generate Key
- Copy the key

### 2. 🔥 Firebase Project
- Go to: https://console.firebase.google.com/
- Create project (FREE!)
- Enable Email/Google auth
- Download credentials

---

## Setup (5 Steps)

### Step 1: Backend Environment
```powershell
cd "c:\Users\gokul\OneDrive\Desktop\mirai\Mirai\backend"
Copy-Item .env.example .env
```

Edit `.env`:
```bash
AWARIO_API_KEY=paste_your_awario_key_here
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
JWT_SECRET_KEY=any_random_32_character_string
```

### Step 2: Firebase Credentials
- Download `firebase-credentials.json` from Firebase
- Save it in `backend/` folder

### Step 3: Frontend Environment
```powershell
cd ..\frontend
Copy-Item .env.example .env
```

Edit `.env`:
```bash
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abcdef
VITE_API_BASE_URL=http://localhost:8000
```

### Step 4: Start Backend
```powershell
cd ..\backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

### Step 5: Frontend Already Running! ✅
```powershell
# Already running at http://localhost:5173
```

---

## Test It!

1. Open: http://localhost:5173
2. Sign up with email or Google
3. Search: "Nike" or "Tesla" or "iPhone"
4. See mentions from Twitter, Facebook, Instagram, etc!

---

## What It Does

**You type:** "Nike"

**Mirai shows you:**
- 📊 Total mentions across all platforms
- 😊 Sentiment (positive/negative/neutral)
- 🔥 Trending hashtags
- 👥 Influencers talking about it
- 📈 Timeline of mentions
- 🌍 Where it's being mentioned

**Just like your Awario screenshot!**

---

## Cost

**Testing (Now):**
- Awario: FREE trial (14 days)
- Firebase: FREE
- Total: $0

**Production (Later):**
- Awario: $29-89/month
- Firebase: FREE
- Total: $29-89/month

---

## Need More Help?

Read these files (in order):
1. `WHAT_YOU_NEED_CHECKLIST.md` - What to get
2. `COMPLETE_SETUP_GUIDE.md` - Detailed setup
3. `HOW_IT_WORKS.md` - Technical details
4. `TROUBLESHOOTING.md` - If stuck

---

## 🎉 That's It!

Your social listening app is ready. Just add the API keys! 🚀
