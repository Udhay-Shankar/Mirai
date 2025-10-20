# Mirai Backend - Node/Express + MongoDB

Professional-grade authentication system with signup/login using MongoDB Atlas.

## Features

- ✅ User signup with email/password
- ✅ Secure login with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ MongoDB Atlas integration
- ✅ Protected routes with auth middleware
- ✅ CORS enabled for frontend

## Setup

1. **Copy environment variables**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and update MongoDB URI** (already configured with your Atlas string)

3. **Install dependencies**
   ```bash
   npm install
   ```

4. **Start the server**
   ```bash
   npm run dev   # Development with nodemon
   # OR
   npm start     # Production
   ```

Server runs on `http://localhost:8000`

## API Endpoints

### POST /api/auth/signup
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "displayName": "John Doe"
}
```

**Response (201):**
```json
{
  "message": "User created successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "displayName": "John Doe",
    "createdAt": "2025-10-20T12:00:00.000Z"
  }
}
```

### POST /api/auth/login
Login with existing credentials.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "displayName": "John Doe",
    "createdAt": "2025-10-20T12:00:00.000Z"
  }
}
```

### GET /api/auth/me
Get current user details (requires authentication).

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Response (200):**
```json
{
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "displayName": "John Doe",
    "createdAt": "2025-10-20T12:00:00.000Z",
    "isVerified": false
  }
}
```

## Testing

Use curl or Postman to test:

**Signup:**
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456","displayName":"Test User"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}'
```

**Get user (replace TOKEN):**
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Security Notes

- Passwords are hashed with bcrypt (10 rounds)
- JWT tokens expire after 7 days
- Email is validated and stored lowercase
- Duplicate emails are prevented
- Minimum password length: 6 characters

## Next Steps

- [ ] Update frontend to use these endpoints
- [ ] Add email verification
- [ ] Add password reset
- [ ] Add rate limiting
- [ ] Add refresh tokens
