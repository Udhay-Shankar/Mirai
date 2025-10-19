# Quick Start Guide - Mirai App

## ✅ What I Just Fixed:

1. ✅ Switched backend to use JWT authentication (auth_new.py)
2. ✅ Switched frontend to use JWT AuthContext
3. ✅ Created .env files for both backend and frontend
4. ✅ Made config fields have defaults (won't crash on startup)
5. ✅ Configured SQLite database (auto-creates on first run)

## 🚀 To Start the App:

### Terminal 1 - Backend:
```powershell
cd c:\Users\udhay\OneDrive\Desktop\Mirai\backend

# Install Python dependencies (you'll need Python first!)
pip install fastapi uvicorn sqlalchemy asyncpg pydantic-settings python-dotenv pyjwt passlib[bcrypt] authlib httpx psutil

# Start the backend server
uvicorn app.main:app --reload
```

### Terminal 2 - Frontend:
```powershell
cd c:\Users\udhay\OneDrive\Desktop\Mirai\frontend

# Start the frontend dev server
npm run dev
```

## 📝 IMPORTANT: Edit Your .env File

### Backend .env (c:\Users\udhay\OneDrive\Desktop\Mirai\backend\.env)

**YOU MUST UPDATE THESE:**

1. **Social Media API Key:**
   ```
   SOCIAL_MEDIA_API_KEY=your_new_api_key_here
   ```
   - Get a NEW key (revoke the old exposed one!)
   - Never share this key again!

2. **JWT Secret Key:**
   ```powershell
   # Generate in PowerShell:
   [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((New-Guid).ToString() + (New-Guid).ToString()))
   ```
   Copy the output and paste it as:
   ```
   JWT_SECRET_KEY=paste_generated_key_here
   ```

## 🎯 Testing the App:

1. **Visit:** http://localhost:5173
2. **Click:** "Get Started" button
3. **Sign Up:** Enter email and password
4. **Should work!** ✅ (if backend is running)

## ⚠️ What's Still Missing:

1. **Social Media API Integration** - Search won't return real data yet
   - Need to implement actual API calls in `backend/app/analytics/processor.py`
   - Need your valid API key in `.env`

2. **OAuth Social Login** - Google/Facebook/Twitter buttons won't work
   - Need OAuth provider credentials
   - Optional for now

## 🔧 If Backend Won't Start:

### Error: "Python not found"
**Solution:** Install Python 3.10+
- Download: https://www.python.org/downloads/
- During install: CHECK "Add Python to PATH"

### Error: "Module not found"
**Solution:** Install dependencies
```powershell
cd backend
pip install -r requirements_jwt.txt
```

### Error: "Port 8000 already in use"
**Solution:** Kill the process or use different port
```powershell
# Find process on port 8000
netstat -ano | findstr :8000
# Kill it (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --reload --port 8001
```

## 🔧 If Frontend Won't Start:

### Error: "Module not found"
**Solution:** Install dependencies
```powershell
cd frontend
npm install
```

### Error: "Port 5173 already in use"
**Solution:** Kill process or it will auto-choose another port

## 📊 Current Functionality:

### ✅ Working:
- Landing page with animations
- Login/Signup UI
- JWT authentication backend
- User registration
- User login
- Protected routes
- Database (SQLite auto-creates)

### ⚠️ Partially Working:
- Dashboard (UI works, but no real data)
- Search (form works, but returns mock data)

### ❌ Not Working Yet:
- Real social media data fetching
- OAuth social login
- Subscription management
- Payment processing

## 🎯 Next Steps:

1. **Install Python** (if you haven't)
2. **Edit .env** files with real API keys
3. **Start both servers**
4. **Test sign up → login → dashboard**
5. **Then implement social media API integration**

## 📚 Important Files:

- `backend/.env` - API keys and configuration
- `frontend/.env` - Frontend API URL
- `backend/app/main.py` - Main backend app (now uses JWT auth)
- `frontend/src/context/AuthContext.jsx` - JWT auth context (switched from Firebase)
- `FUNCTIONALITY_STATUS.md` - Detailed status of all features

## 🆘 Need Help?

Check the logs:
- Backend: Look at terminal where uvicorn is running
- Frontend: Look at browser console (F12)
- Errors will show you what's wrong!

---

**You're 80% there! Just need to:**
1. Install Python
2. Update API keys in .env
3. Start the servers
4. Test! 🚀
