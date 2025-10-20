# ✅ MIRAI - What You Need Checklist

## 🎯 Before You Can Run the App

### 1. Awario API Key (CRITICAL!) 🔑

**Status:** ❌ NOT YET CONFIGURED

**What it is:** The key that lets your app access Awario's web scraping service

**How to get:**
1. Go to https://awario.com/
2. Sign up for account
3. Start free trial (7-14 days FREE!)
4. Go to Settings → API
5. Generate API Key
6. Copy the key

**Cost:**
- ✅ Free Trial: 7-14 days
- Starter: $29/month
- Pro: $89/month

**Where to put it:**
- File: `backend/.env`
- Variable: `AWARIO_API_KEY=your_key_here`

---

### 2. Firebase Project (For User Login) 🔥

**Status:** ❌ NOT YET CONFIGURED

**What it is:** Google's service for user authentication (login/signup)

**How to get:**
1. Go to https://console.firebase.google.com/
2. Create new project
3. Enable Authentication (Email, Google)
4. Download Admin SDK JSON file
5. Copy web config values

**Cost:**
- ✅ FREE forever for small apps!

**Where to put it:**

**Backend:**
- File: `backend/firebase-credentials.json` (the JSON file you download)
- File: `backend/.env`
- Variable: `FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json`

**Frontend:**
- File: `frontend/.env`
- Variables:
  ```
  VITE_FIREBASE_API_KEY=...
  VITE_FIREBASE_AUTH_DOMAIN=...
  VITE_FIREBASE_PROJECT_ID=...
  VITE_FIREBASE_STORAGE_BUCKET=...
  VITE_FIREBASE_MESSAGING_SENDER_ID=...
  VITE_FIREBASE_APP_ID=...
  ```

---

### 3. Python & Node.js (Already Installed?) ✅

**Check if installed:**

Open PowerShell and run:
```powershell
python --version   # Should show 3.9 or higher
node --version     # Should show 16 or higher
npm --version      # Should show 8 or higher
```

If not installed:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

---

## 📋 Configuration Checklist

### Backend Configuration

- [ ] Navigate to `backend/` folder
- [ ] Create `.env` file (copy from `.env.example`)
- [ ] Add Awario API key to `.env`
- [ ] Download Firebase Admin JSON and save as `firebase-credentials.json`
- [ ] Update `FIREBASE_CREDENTIALS_PATH` in `.env`
- [ ] Generate random secret for `JWT_SECRET_KEY`
- [ ] Install Python dependencies: `pip install -r requirements.txt`

### Frontend Configuration

- [ ] Navigate to `frontend/` folder
- [ ] Create `.env` file (copy from `.env.example`)
- [ ] Add Firebase config values to `.env`
- [ ] Set `VITE_API_BASE_URL=http://localhost:8000`
- [ ] Dependencies already installed ✅

---

## 🚀 Ready to Run?

Once all checkboxes are ✅, run these commands:

**Terminal 1 (Backend):**
```powershell
cd "c:\Users\gokul\OneDrive\Desktop\mirai\Mirai\backend"
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```powershell
cd "c:\Users\gokul\OneDrive\Desktop\mirai\Mirai\frontend"
npm run dev
```

**Then open:** http://localhost:5173

---

## 🎯 Quick Summary

**MUST HAVE:**
1. ✅ Awario API key (get free trial)
2. ✅ Firebase project (100% free)
3. ✅ Configure `.env` files

**NICE TO HAVE:**
- Firebase Google/Facebook login (optional)
- Custom domain (later)
- Payment integration (later)

---

## 💰 Cost Breakdown

**Development/Testing:**
- Awario: FREE trial (14 days)
- Firebase: FREE forever
- Hosting locally: FREE
- **Total: $0**

**Production (monthly):**
- Awario: $29-89/month (depends on usage)
- Firebase: FREE (up to 10K users)
- Backend hosting: $5-10/month (Heroku, Railway, etc.)
- Frontend hosting: FREE (Vercel, Netlify)
- **Total: ~$34-99/month**

---

## ❓ FAQ

**Q: Can I test without Awario API key?**
A: No, the app won't work without it. But the free trial is easy to get!

**Q: Do I need a credit card for Firebase?**
A: No! Firebase is completely free for small projects.

**Q: Can I use a different auth system instead of Firebase?**
A: Yes, but you'd need to rewrite the auth code. Firebase is easiest.

**Q: How long does setup take?**
A: 15-30 minutes if you follow the guide step by step.

**Q: Can I deploy this for clients?**
A: Yes! You'd pay for Awario API based on usage, then charge your clients.

---

## 📞 Still Stuck?

Read the **COMPLETE_SETUP_GUIDE.md** for detailed instructions!
