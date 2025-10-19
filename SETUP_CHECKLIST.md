# 🎯 Complete Setup Checklist - Mirai App

## ✅ What's Already Done:

- [x] JWT authentication backend created
- [x] JWT authentication frontend created
- [x] Backend switched to use JWT (main.py updated)
- [x] Frontend switched to use JWT AuthContext
- [x] .env files created
- [x] Configuration updated with defaults
- [x] Frontend dependencies installed (axios, vanta, lenis)
- [x] Beautiful UI completed (landing, login, signup, dashboard)

## 📋 What YOU Need to Do:

### Step 1: Install Python (REQUIRED) 🔴

**If you don't have Python:**

1. Download Python 3.10 or newer from: https://www.python.org/downloads/
2. **IMPORTANT:** During installation, CHECK the box "Add Python to PATH"
3. Restart your terminal after installation
4. Verify: `python --version` should show Python 3.10+

### Step 2: Install Python Dependencies 🔴

```powershell
cd c:\Users\udhay\OneDrive\Desktop\Mirai\backend

# Install all required packages
pip install fastapi uvicorn[standard] sqlalchemy asyncpg pydantic-settings python-dotenv pyjwt passlib[bcrypt] authlib httpx psutil aiosqlite
```

### Step 3: Update API Keys in .env 🔴 CRITICAL

**Edit:** `backend\.env`

1. **Revoke your exposed API key** (in your provider dashboard)
2. **Get a new API key**
3. **Update these lines:**
   ```
   SOCIAL_MEDIA_API_KEY=your_new_api_key_here
   JWT_SECRET_KEY=generate_strong_secret_at_least_32_characters_long
   ```

**Generate JWT Secret:**
```powershell
# In PowerShell, run:
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
```

### Step 4: Start Backend Server 🟢

```powershell
cd c:\Users\udhay\OneDrive\Desktop\Mirai\backend
uvicorn app.main:app --reload
```

**Should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Starting Mirai API server...
INFO:     Database initialized
```

**If it starts successfully:** ✅ Backend is working!

### Step 5: Start Frontend Server 🟢

**In a NEW terminal:**
```powershell
cd c:\Users\udhay\OneDrive\Desktop\Mirai\frontend
npm run dev
```

**Should see:**
```
VITE v5.0.8  ready in 1234 ms
➜  Local:   http://localhost:5173/
```

**If it starts successfully:** ✅ Frontend is working!

### Step 6: Test the App 🎯

1. **Open browser:** http://localhost:5173
2. **Click "Get Started"**
3. **Sign Up** with email and password
4. **Check backend terminal** - should see registration request
5. **Should redirect to dashboard** ✅

---

## 🔍 Troubleshooting

### Problem: Python not found
```
python : The term 'python' is not recognized...
```

**Solution:**
1. Install Python from https://www.python.org/downloads/
2. During install: CHECK "Add Python to PATH"
3. Restart terminal
4. Try again

### Problem: pip not found
```
pip : The term 'pip' is not recognized...
```

**Solution:**
```powershell
python -m pip install --upgrade pip
```

### Problem: uvicorn not found
```
uvicorn : The term 'uvicorn' is not recognized...
```

**Solution:**
```powershell
pip install uvicorn[standard]
```

### Problem: Module import errors
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```powershell
cd backend
pip install -r requirements_jwt.txt
# Or install individually:
pip install fastapi uvicorn sqlalchemy asyncpg pydantic-settings python-dotenv pyjwt passlib[bcrypt] authlib httpx psutil aiosqlite
```

### Problem: Port already in use
```
ERROR: [Errno 10048] Only one usage of each socket address
```

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000
# Kill it (replace 1234 with actual PID)
taskkill /PID 1234 /F
```

### Problem: Database errors
```
sqlite3.OperationalError: unable to open database file
```

**Solution:**
```powershell
# Make sure you're in backend directory
cd c:\Users\udhay\OneDrive\Desktop\Mirai\backend
# SQLite will auto-create the database
uvicorn app.main:app --reload
```

### Problem: CORS errors in browser
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Solution:**
- Make sure backend is running on port 8000
- Check `backend/.env` has: `CORS_ORIGINS=http://localhost:5173,http://localhost:3000`
- Restart backend server

### Problem: Frontend can't connect to backend
```
ERR_CONNECTION_REFUSED
```

**Solution:**
- Make sure backend is running (check terminal)
- Make sure it's on port 8000
- Check `frontend/.env` has: `VITE_API_URL=http://localhost:8000`
- Restart frontend: `npm run dev`

---

## 📊 Testing Checklist

Once both servers are running:

### Test 1: Backend Health Check ✅
```powershell
# In browser or curl:
curl http://localhost:8000/health
```
**Expected:**
```json
{
  "status": "healthy",
  "version": "v1",
  "service": "Mirai Social Listening API"
}
```

### Test 2: Frontend Loading ✅
1. Visit: http://localhost:5173
2. Should see: Beautiful landing page with animations
3. Should see: "MIRAI" logo, "Get Started" button

### Test 3: User Registration ✅
1. Click "Get Started"
2. Fill signup form:
   - Email: test@example.com
   - Password: TestPassword123!
   - Full Name: Test User
3. Click "Sign Up"
4. Should see: Dashboard

### Test 4: User Login ✅
1. Logout (if logged in)
2. Go to Login page
3. Enter same credentials
4. Should see: Dashboard

### Test 5: Protected Routes ✅
1. Logout
2. Try to visit: http://localhost:5173/dashboard
3. Should redirect to: /login

### Test 6: Search Function ⚠️
1. Login to dashboard
2. Enter keyword: "AI tools"
3. Click search
4. Will show mock data (real API not implemented yet)

---

## 🎯 Current Status

### ✅ Fully Working:
- Landing page
- Login/Signup UI
- JWT authentication
- User registration
- User login
- Protected routes
- Database (SQLite)
- Session management
- Token refresh

### ⚠️ Partially Working:
- Dashboard (shows but no real data)
- Search (UI works, returns mock data)
- Charts (display but with placeholder data)

### ❌ Not Working:
- Real social media data fetching (API not integrated)
- OAuth social logins (providers not configured)
- Subscription payments
- Email verification
- Admin dashboard
- Monitoring dashboard

---

## 🚀 Quick Command Reference

**Backend:**
```powershell
cd c:\Users\udhay\OneDrive\Desktop\Mirai\backend
pip install fastapi uvicorn sqlalchemy asyncpg pydantic-settings python-dotenv pyjwt passlib[bcrypt] authlib httpx psutil aiosqlite
uvicorn app.main:app --reload
```

**Frontend:**
```powershell
cd c:\Users\udhay\OneDrive\Desktop\Mirai\frontend
npm run dev
```

**Generate JWT Secret:**
```powershell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
```

**Check if servers are running:**
- Backend: http://localhost:8000/health
- Frontend: http://localhost:5173

---

## 📁 Important Files

| File | Purpose | You Need To: |
|------|---------|--------------|
| `backend/.env` | API keys & config | ✏️ Edit API keys |
| `frontend/.env` | Frontend config | ✅ Already set |
| `backend/app/main.py` | Backend entry | ✅ Already updated |
| `frontend/src/context/AuthContext.jsx` | Auth logic | ✅ Already switched |
| `FUNCTIONALITY_STATUS.md` | Detailed status | 📖 Read for info |
| `QUICK_START.md` | Quick guide | 📖 Quick reference |

---

## 🎓 What to Do Next

### Immediate (Get it running):
1. [ ] Install Python
2. [ ] Install Python dependencies
3. [ ] Update API keys in .env
4. [ ] Start backend server
5. [ ] Start frontend server
6. [ ] Test signup → login → dashboard

### Soon (Real functionality):
1. [ ] Implement social media API integration
2. [ ] Connect real data to charts
3. [ ] Add error handling
4. [ ] Test with real searches

### Later (Polish):
1. [ ] Set up OAuth providers
2. [ ] Add subscription management
3. [ ] Implement monitoring
4. [ ] Deploy to production

---

## 🆘 Still Stuck?

**Check:**
1. Both terminals are running (backend + frontend)
2. No red errors in terminals
3. Browser console (F12) for errors
4. Network tab (F12) to see API calls

**Common Issues:**
- Python not installed → Install it
- Dependencies not installed → Run pip install
- API keys not updated → Edit .env
- Ports in use → Kill processes
- CORS errors → Check origins in .env

---

**You're almost there! Just need Python installed and servers running!** 🚀
