# Mirai Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] Awario API account and API key
- [ ] Firebase project created
- [ ] Firebase Authentication enabled (Google, Facebook, Email, Phone)

## Quick Start (5 minutes)

### 1. Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item .env.example .env

# Edit .env and add your credentials:
# - AWARIO_API_KEY=your_key
# - FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
# - JWT_SECRET_KEY=your_secret_32_chars_minimum

# Download Firebase credentials JSON from Firebase Console
# Place it in the backend directory as firebase-credentials.json

# Run backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
API docs: http://localhost:8000/docs

### 2. Frontend Setup (in a new terminal)

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
Copy-Item .env.example .env

# Edit .env and add your Firebase config from Firebase Console

# Run frontend dev server
npm run dev
```

Frontend will be available at: http://localhost:5173

## Testing the Application

### 1. Test Free Features
1. Open http://localhost:5173
2. Click "Get Started" or "Sign Up"
3. Sign up with Google/Facebook/Email
4. Enter a keyword (e.g., "Nike", "Tesla")
5. Click "Search"
6. You should see:
   - Total mentions count
   - Sentiment breakdown
   - Top 5 keywords
   - Source breakdown

### 2. Test Premium Features
To test premium features, you need to upgrade the account:

**Option A: Via Database (for testing)**
```powershell
# In backend directory
python -c "from app.database import *; from app.models import *; import asyncio; asyncio.run(upgrade_user_to_premium())"
```

**Option B: Via API**
Use the Swagger UI at http://localhost:8000/docs:
1. Authenticate using your token
2. Call POST `/api/subscription/upgrade`
3. Pass `{"tier": "premium"}`

After upgrading, you'll see:
- Extended date range (30 days)
- Full influencer lists
- Trend charts and time series
- Engagement metrics
- Export functionality

## Common Issues & Solutions

### Issue: "Module not found" errors in Python
**Solution**: Make sure virtual environment is activated
```powershell
cd backend
.\venv\Scripts\Activate.ps1
```

### Issue: Firebase authentication not working
**Solution**: 
1. Check Firebase config in frontend/.env
2. Verify authentication methods are enabled in Firebase Console
3. Add localhost:5173 to authorized domains in Firebase

### Issue: CORS errors
**Solution**: 
1. Check CORS_ORIGINS in backend/.env includes http://localhost:5173
2. Restart backend server

### Issue: Awario API errors
**Solution**:
1. Verify API key is correct in backend/.env
2. Check Awario API status
3. Review rate limits

## Project Structure

```
Mirai/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── config.py       # Configuration
│   │   ├── models.py       # Database models
│   │   ├── auth/           # Authentication
│   │   ├── awario/         # Awario API client
│   │   ├── analytics/      # Data processing
│   │   └── routers/        # API endpoints
│   └── tests/              # Unit tests
│
└── frontend/               # React + Vite frontend
    └── src/
        ├── components/     # React components
        ├── context/        # React context
        └── services/       # API services

## Running Tests

### Backend Tests
```powershell
cd backend
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests
```powershell
cd frontend
npm test
```

## Production Deployment

### Backend (Example: Heroku)
```powershell
heroku create mirai-backend
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set AWARIO_API_KEY=your_key
heroku config:set JWT_SECRET_KEY=your_secret
git subtree push --prefix backend heroku main
```

### Frontend (Example: Vercel)
```powershell
cd frontend
vercel --prod
```

## Environment Variables Reference

### Backend (.env)
```
AWARIO_API_KEY=            # From Awario dashboard
FIREBASE_CREDENTIALS_PATH= # Path to Firebase JSON
JWT_SECRET_KEY=            # Random 32+ char string
DATABASE_URL=              # Database connection string
CORS_ORIGINS=              # Comma-separated frontend URLs
```

### Frontend (.env)
```
VITE_FIREBASE_API_KEY=     # From Firebase Console
VITE_FIREBASE_AUTH_DOMAIN= # your-app.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=  # your-project-id
VITE_FIREBASE_STORAGE_BUCKET=
VITE_FIREBASE_MESSAGING_SENDER_ID=
VITE_FIREBASE_APP_ID=
VITE_API_BASE_URL=         # Backend URL
```

## Support

For issues:
1. Check the main README.md
2. Review API documentation at /docs
3. Check browser console and backend logs
4. Create an issue on GitHub

## Next Steps

1. Customize brand colors in tailwind.config.js
2. Add your logo/branding
3. Configure payment processing for subscriptions
4. Set up production database (PostgreSQL)
5. Configure CI/CD pipeline
6. Set up monitoring and logging
7. Add email notifications
8. Implement data export features

## Security Checklist

- [ ] Change JWT_SECRET_KEY to a strong random value
- [ ] Never commit .env files
- [ ] Use HTTPS in production
- [ ] Set up rate limiting (already included)
- [ ] Configure Firebase security rules
- [ ] Set up backup strategy
- [ ] Enable logging and monitoring
- [ ] Review and update dependencies regularly

Enjoy using Mirai! 🚀
