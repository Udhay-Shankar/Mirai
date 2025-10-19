# Mirai Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Issue: "Python not recognized"
**Cause**: Python not in system PATH

**Solution**:
1. Download Python from https://python.org
2. During installation, check "Add Python to PATH"
3. Restart terminal/command prompt
4. Verify: `python --version`

#### Issue: "npm not found"
**Cause**: Node.js not installed or not in PATH

**Solution**:
1. Download Node.js from https://nodejs.org
2. Install and restart terminal
3. Verify: `node --version` and `npm --version`

#### Issue: "pip install fails with permission error"
**Solution**:
```powershell
# Use virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Backend Issues

#### Issue: "ModuleNotFoundError: No module named 'app'"
**Cause**: Running from wrong directory or venv not activated

**Solution**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

#### Issue: "ValueError: Firebase credentials not found"
**Cause**: Missing or incorrect Firebase credentials file

**Solution**:
1. Go to Firebase Console → Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Save as `firebase-credentials.json` in backend directory
4. Update `FIREBASE_CREDENTIALS_PATH` in `.env`

#### Issue: "AwarioAuthenticationError: Invalid API key"
**Cause**: Incorrect or missing Awario API key

**Solution**:
1. Log in to Awario dashboard
2. Navigate to API settings
3. Copy your API key
4. Update `AWARIO_API_KEY` in `backend/.env`

#### Issue: "Database locked" error
**Cause**: SQLite database accessed by multiple processes

**Solution**:
```powershell
# Stop all backend processes
# Delete database file
rm backend/mirai.db
# Restart backend (will recreate database)
```

#### Issue: Port 8000 already in use
**Solution**:
```powershell
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --reload --port 8001
```

---

### Frontend Issues

#### Issue: "Module not found" in React
**Cause**: Dependencies not installed

**Solution**:
```powershell
cd frontend
npm install
```

#### Issue: "Firebase app already exists"
**Cause**: Multiple Firebase initializations

**Solution**:
- Already handled in code with conditional check
- If persists, clear browser cache and localStorage

#### Issue: "CORS policy error"
**Cause**: Backend not allowing frontend origin

**Solution**:
1. Check `backend/.env` has correct `CORS_ORIGINS`
   ```
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   ```
2. Restart backend server
3. Clear browser cache

#### Issue: "Failed to fetch" or network errors
**Cause**: Backend not running or wrong URL

**Solution**:
1. Ensure backend is running at http://localhost:8000
2. Check `VITE_API_BASE_URL` in `frontend/.env`
3. Test backend directly: http://localhost:8000/docs

#### Issue: Port 5173 already in use
**Solution**:
```powershell
# Edit vite.config.js to change port
server: {
  port: 3000  // or any available port
}
```

---

### Authentication Issues

#### Issue: "Invalid or expired token"
**Cause**: Firebase token expired or authentication state issue

**Solution**:
1. Logout and login again
2. Clear browser localStorage:
   ```javascript
   localStorage.clear()
   ```
3. Refresh page

#### Issue: Google/Facebook login popup blocked
**Cause**: Browser popup blocker

**Solution**:
1. Allow popups for localhost
2. Or use redirect method instead of popup

#### Issue: "User not found in database"
**Cause**: User authenticated in Firebase but not in backend DB

**Solution**:
1. Backend should auto-register on first login
2. Check backend logs for errors
3. Verify Firebase credentials are correct

#### Issue: Phone authentication not working
**Cause**: reCAPTCHA not configured

**Solution**:
1. Enable reCAPTCHA in Firebase Console
2. Add site key to frontend
3. Configure reCAPTCHA container in signup component

---

### API Issues

#### Issue: "Rate limit exceeded"
**Cause**: Too many requests in short time

**Solution**:
- Wait 60 seconds before retrying
- For testing, temporarily increase `RATE_LIMIT_PER_MINUTE` in `.env`
- Upgrade to premium for higher limits

#### Issue: "Premium subscription required"
**Cause**: Accessing premium endpoint with free account

**Solution**:
- Upgrade account via dashboard
- Or for testing, manually update database:
  ```sql
  UPDATE users SET subscription_tier='premium' WHERE email='your@email.com';
  ```

#### Issue: Awario API returns empty data
**Possible Causes**:
1. No mentions found for keyword (try popular brand names)
2. Date range too narrow
3. API rate limits

**Solution**:
- Try different keywords
- Extend date range
- Check Awario dashboard for data availability

---

### Build & Deployment Issues

#### Issue: Frontend build fails
**Cause**: Syntax errors or dependency issues

**Solution**:
```powershell
# Clear cache and rebuild
rm -rf node_modules dist
npm install
npm run build
```

#### Issue: "Cannot find module" in production
**Cause**: Missing dependencies or wrong NODE_ENV

**Solution**:
```powershell
# Ensure all dependencies are in dependencies, not devDependencies
npm install --production
```

#### Issue: Environment variables not working in production
**Cause**: Vite environment variables must be prefixed with `VITE_`

**Solution**:
- Ensure all frontend env vars start with `VITE_`
- Set environment variables in deployment platform
- Rebuild after changing env vars

---

### Database Issues

#### Issue: "Table does not exist"
**Cause**: Database not initialized

**Solution**:
```python
# Run from backend directory
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

#### Issue: Database migration errors
**Cause**: Schema changes

**Solution**:
- For development: Delete database and reinitialize
- For production: Use Alembic migrations (not included, but recommended)

---

### Performance Issues

#### Issue: Slow API responses
**Possible Causes**:
1. Large dataset
2. No pagination
3. Network latency to Awario API

**Solution**:
- Use pagination parameters
- Implement caching (Redis)
- Optimize database queries
- Add loading indicators in UI

#### Issue: Frontend slow or laggy
**Cause**: Large data rendering

**Solution**:
- Use pagination in lists
- Implement virtual scrolling for long lists
- Lazy load charts
- Optimize re-renders with React.memo

---

### Testing Issues

#### Issue: Tests fail with "No module named 'app'"
**Cause**: Running tests from wrong directory

**Solution**:
```powershell
cd backend
pytest tests/ -v
```

#### Issue: "fixture 'event_loop' not found"
**Cause**: pytest-asyncio configuration issue

**Solution**:
- Already configured in `pytest.ini`
- Ensure pytest-asyncio is installed: `pip install pytest-asyncio`

---

## Debug Mode

### Enable Backend Debug Logging
Edit `backend/.env`:
```
DEBUG_MODE=True
```

Check logs for detailed error messages.

### Enable Frontend Debug Mode
Open browser DevTools:
- Console: See React errors and API calls
- Network: Monitor API requests/responses
- Application: Check localStorage and cookies

---

## Getting Help

If you're still stuck:

1. **Check Documentation**
   - README.md
   - QUICKSTART.md
   - API_DOCUMENTATION.md

2. **Review Logs**
   - Backend: Terminal output
   - Frontend: Browser console
   - Network: Browser DevTools Network tab

3. **Verify Configuration**
   - All environment variables set
   - Firebase credentials valid
   - Awario API key valid

4. **Test Components Individually**
   - Can you access http://localhost:8000/health ?
   - Does http://localhost:8000/docs work?
   - Can you login to Firebase Console?

5. **Search Issues**
   - Check GitHub issues
   - Search Stack Overflow
   - Check Firebase and FastAPI docs

6. **Ask for Help**
   - Create detailed GitHub issue
   - Include error messages
   - Include logs
   - Include configuration (without secrets!)

---

## Clean Restart

If all else fails, try a complete restart:

```powershell
# Backend
cd backend
rm -rf venv mirai.db __pycache__
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules dist
npm install

# Reconfigure
# 1. backend/.env
# 2. backend/firebase-credentials.json
# 3. frontend/.env

# Restart servers
cd backend
uvicorn app.main:app --reload

cd frontend
npm run dev
```

---

## Preventive Measures

### Before Reporting Issues
- [ ] Read error message carefully
- [ ] Check spelling in config files
- [ ] Verify all environment variables are set
- [ ] Ensure backend is running before testing frontend
- [ ] Try in incognito/private browser window
- [ ] Check firewall/antivirus isn't blocking ports

### Best Practices
- Keep dependencies updated
- Use version control (git)
- Don't commit secrets
- Test in clean environment
- Document custom changes
- Keep backups

---

## Quick Diagnostic Commands

### Check Services
```powershell
# Check if backend is running
curl http://localhost:8000/health

# Check if frontend is running
curl http://localhost:5173
```

### Check Configuration
```powershell
# Backend
cd backend
python -c "from app.config import settings; print(settings)"

# Frontend
cd frontend
npm run build  # Will fail if config issues
```

### Test API
```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test with authentication
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/auth/me
```

---

## Error Code Reference

### HTTP Status Codes
- **400**: Bad request - Check request body/parameters
- **401**: Unauthorized - Token invalid/missing
- **403**: Forbidden - Insufficient permissions (upgrade needed)
- **404**: Not found - Check URL/endpoint
- **429**: Rate limited - Wait and retry
- **500**: Server error - Check backend logs
- **503**: Service unavailable - Check Awario API status

---

Remember: Most issues are configuration-related. Double-check your `.env` files!
