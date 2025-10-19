# JWT + OAuth Authentication Setup Guide

## Overview
This guide will help you migrate from Firebase authentication to a fully open-source JWT + OAuth authentication system.

## Features
- ✅ **Email/Password Authentication** with bcrypt password hashing
- ✅ **JWT Tokens**: Access tokens (24h) + Refresh tokens (30 days)
- ✅ **OAuth 2.0 Support**: Google, Facebook, Twitter/X, Instagram
- ✅ **Secure**: Industry-standard security practices
- ✅ **Open Source**: No vendor lock-in, full control

---

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements_jwt.txt
```

Or install individually:
```bash
pip install PyJWT==2.8.0 passlib[bcrypt]==1.7.4 bcrypt==4.1.2 python-jose[cryptography]==3.3.0 Authlib==1.3.0 httpx==0.25.2
```

### 2. Environment Variables

Create/update your `.env` file:

```env
# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS=30

# OAuth Provider Credentials

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Facebook OAuth
FACEBOOK_CLIENT_ID=your-facebook-app-id
FACEBOOK_CLIENT_SECRET=your-facebook-app-secret

# Twitter OAuth 2.0
TWITTER_CLIENT_ID=your-twitter-client-id
TWITTER_CLIENT_SECRET=your-twitter-client-secret

# Instagram OAuth (via Facebook)
INSTAGRAM_CLIENT_ID=your-instagram-app-id
INSTAGRAM_CLIENT_SECRET=your-instagram-app-secret

# Frontend URL for OAuth redirects
FRONTEND_URL=http://localhost:5173

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mirai
```

**⚠️ IMPORTANT**: Generate a strong SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. OAuth Provider Setup

#### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Application type: "Web application"
6. Authorized redirect URIs: `http://localhost:8000/api/auth/oauth/google/callback`
7. Copy Client ID and Client Secret to `.env`

#### Facebook OAuth
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app → "Consumer" type
3. Add "Facebook Login" product
4. Settings → Valid OAuth Redirect URIs: `http://localhost:8000/api/auth/oauth/facebook/callback`
5. Copy App ID and App Secret to `.env`

#### Twitter OAuth 2.0
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project and app
3. User authentication settings → OAuth 2.0
4. Type: "Web App"
5. Callback URI: `http://localhost:8000/api/auth/oauth/twitter/callback`
6. Copy Client ID and Client Secret to `.env`

#### Instagram OAuth
1. Uses Facebook OAuth (Instagram is owned by Meta)
2. In Facebook Developers, add "Instagram Basic Display" product
3. Same callback as Facebook: `http://localhost:8000/api/auth/oauth/instagram/callback`
4. Use same credentials as Facebook app

### 4. Database Migration

Run the migration script to update your database schema:

```bash
# Using psql
psql -U your_user -d mirai -f migrations/001_jwt_auth_migration.sql

# Or using Python/SQLAlchemy
python
>>> from app.database import engine
>>> from app.models import Base
>>> Base.metadata.create_all(bind=engine)
```

**Migration includes:**
- Adds `password_hash` column for email/password auth
- Adds `full_name` column (replaces `display_name`)
- Adds `provider_user_id` for OAuth provider IDs
- Makes `firebase_uid` nullable for backward compatibility
- Creates indexes for performance

### 5. Update Main Application

Replace the old auth router with the new one:

**In `app/main.py`:**

```python
# OLD (remove this)
# from app.routers import auth

# NEW (add this)
from app.routers import auth_new as auth

# ... rest of your code
app.include_router(auth.router)
```

### 6. Start Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install axios
```

### 2. Environment Variables

Create/update `.env` in frontend:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Replace AuthContext

**Option A: Direct replacement**
```bash
# Backup old AuthContext
mv src/context/AuthContext.jsx src/context/AuthContext_Firebase.jsx.bak

# Use new JWT AuthContext
mv src/context/AuthContext_JWT.jsx src/context/AuthContext.jsx
```

**Option B: Update imports**
In all files that import `AuthContext`, update the import:
```jsx
// Change all imports from:
import { useAuth } from './context/AuthContext';

// To:
import { useAuth } from './context/AuthContext_JWT';
```

### 4. Update Login/Signup Components

The Login and Signup components should work with minimal changes. Just ensure they're using the correct methods:

**Login.jsx:**
```jsx
const { signInWithEmail, signInWithGoogle, signInWithFacebook, signInWithTwitter } = useAuth();

// Email login
await signInWithEmail(email, password);

// Social login
signInWithGoogle(); // This will redirect
```

**Signup.jsx:**
```jsx
const { signUpWithEmail } = useAuth();

await signUpWithEmail(email, password, fullName);
```

### 5. Handle OAuth Callback

The AuthContext automatically handles OAuth callbacks. When users are redirected back from OAuth providers, they'll be automatically logged in and redirected to `/dashboard`.

### 6. Protected Routes

Update your protected routes to use the new auth:

```jsx
import { Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  return isAuthenticated() ? children : <Navigate to="/login" />;
};
```

### 7. Start Frontend

```bash
cd frontend
npm run dev
```

---

## Testing the Authentication

### 1. Email/Password Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!",
    "full_name": "Test User"
  }'
```

### 2. Email/Password Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'
```

### 3. Test OAuth Flow
1. Navigate to `http://localhost:5173/login`
2. Click "Sign in with Google" (or other provider)
3. Complete OAuth flow
4. Should redirect back and be logged in

### 4. Verify Token
```bash
# Use the access_token from login response
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 5. Refresh Token
```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN_HERE"
  }'
```

---

## Security Best Practices

### Production Checklist

✅ **Use HTTPS in production** - No exceptions!
✅ **Strong SECRET_KEY** - Generate with `secrets.token_urlsafe(32)`
✅ **Secure token storage** - Use httpOnly cookies in production (better than localStorage)
✅ **Rate limiting** - Add rate limiting to auth endpoints
✅ **CORS configuration** - Only allow your frontend domain
✅ **Token rotation** - Implement refresh token rotation
✅ **Password requirements** - Enforce strong passwords (min 8 chars, mix of types)
✅ **Account lockout** - Implement after N failed login attempts
✅ **Email verification** - Add email verification for new accounts
✅ **2FA** - Consider adding two-factor authentication

### Environment-Specific URLs

**Development:**
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- OAuth Callbacks: `http://localhost:8000/api/auth/oauth/{provider}/callback`

**Production:**
- Backend: `https://api.yourdomain.com`
- Frontend: `https://yourdomain.com`
- OAuth Callbacks: `https://api.yourdomain.com/api/auth/oauth/{provider}/callback`
- **Update all OAuth provider callback URLs in their consoles!**

---

## API Endpoints Reference

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register with email/password |
| POST | `/api/auth/login` | Login with email/password |
| POST | `/api/auth/refresh` | Refresh access token |
| GET | `/api/auth/me` | Get current user info |
| POST | `/api/auth/logout` | Logout user |
| GET | `/api/auth/oauth/{provider}` | Initiate OAuth flow |
| GET | `/api/auth/oauth/{provider}/callback` | OAuth callback handler |

### Request/Response Examples

**Register:**
```json
// Request
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}

// Response
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "provider": "email",
    "subscription_tier": "free"
  }
}
```

---

## Troubleshooting

### Common Issues

**Issue: "Invalid token"**
- Solution: Token might be expired. Use refresh token to get new access token.

**Issue: OAuth callback fails**
- Solution: Check that callback URLs match exactly in provider console and your code.

**Issue: "CORS error"**
- Solution: Add frontend URL to CORS allowed origins in FastAPI.

**Issue: Token not persisting**
- Solution: Check localStorage in browser DevTools. Ensure tokens are being saved.

**Issue: Database errors**
- Solution: Run the migration script to update schema.

---

## Migration from Firebase

### Step-by-Step Migration

1. **Keep Firebase running** - Don't remove Firebase yet
2. **Deploy new auth system** - Run in parallel
3. **Create migration script** - Convert Firebase users to JWT users:

```python
# migration_script.py
import firebase_admin
from firebase_admin import auth as firebase_auth
from app.database import SessionLocal
from app.models import User
from app.auth.jwt_handler import jwt_handler

def migrate_firebase_users():
    db = SessionLocal()
    
    # Get all Firebase users
    firebase_users = firebase_auth.list_users().users
    
    for fb_user in firebase_users:
        # Check if already migrated
        existing = db.query(User).filter(User.firebase_uid == fb_user.uid).first()
        
        if not existing:
            # Create new user with JWT auth
            new_user = User(
                email=fb_user.email,
                full_name=fb_user.display_name,
                photo_url=fb_user.photo_url,
                firebase_uid=fb_user.uid,  # Keep for reference
                provider=fb_user.provider_id,
                is_active=True
            )
            db.add(new_user)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    migrate_firebase_users()
```

4. **Test thoroughly** - Ensure all auth flows work
5. **Update production OAuth URLs** - In all provider consoles
6. **Deploy** - Push to production
7. **Monitor** - Watch for errors
8. **Deprecate Firebase** - After successful migration

---

## Support

If you encounter issues:
1. Check console logs (browser and backend)
2. Verify environment variables are set correctly
3. Ensure database migration completed successfully
4. Check OAuth provider settings match exactly

---

## License
Open source under MIT License
