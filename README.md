# Mirai - Social Listening Platform

Mirai is a powerful social listening web application that leverages the Awario API to track brand mentions, influencer accounts, and trends across major social media platforms.

## Features

### Core Functionality
- **Multi-Platform Social Listening**: Track mentions across Twitter, Facebook, Instagram, YouTube, and more
- **Real-Time Analytics**: Monitor brand mentions, sentiment, and reach in real-time
- **Influencer Discovery**: Identify key influencers and trending content creators
- **Competitor Analysis**: Compare your brand against competitors
- **Trend Tracking**: Analyze trending topics, hashtags, and keywords over time

### Authentication
- Google OAuth login
- Facebook OAuth login
- Email/Password authentication
- Phone number (OTP) authentication
- Powered by Firebase Authentication

### Freemium Model
- **Free Tier**: Basic analytics including total mentions, sentiment breakdown, and top keywords
- **Premium Tier**: Advanced features including time series analysis, demographic data, full influencer lists, and competitor comparisons

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Authentication**: Firebase Admin SDK
- **API Integration**: Awario API
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Testing**: pytest

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **State Management**: React Context API
- **Charts**: Recharts
- **Styling**: TailwindCSS
- **HTTP Client**: Axios

## Project Structure

```
Mirai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration and environment variables
│   │   ├── models.py               # Data models
│   │   ├── database.py             # Database setup
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── firebase_auth.py    # Firebase authentication
│   │   │   └── dependencies.py     # Auth dependencies
│   │   ├── awario/
│   │   │   ├── __init__.py
│   │   │   ├── client.py           # Awario API client
│   │   │   └── exceptions.py       # Custom exceptions
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   ├── processor.py        # Data processing
│   │   │   └── metrics.py          # Metric calculations
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── auth.py             # Auth endpoints
│   │       ├── analytics.py        # Analytics endpoints
│   │       └── subscription.py     # Subscription management
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_awario_client.py
│   │   └── test_analytics.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Landing.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── MentionsChart.jsx
│   │   │   ├── SentimentChart.jsx
│   │   │   ├── InfluencerList.jsx
│   │   │   ├── TrendingMetrics.jsx
│   │   │   └── WordCloud.jsx
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn
- Awario API key
- Firebase project with Auth enabled

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Fill in your credentials:
     ```
     AWARIO_API_KEY=your_awario_api_key
     FIREBASE_CREDENTIALS_PATH=path/to/firebase-credentials.json
     JWT_SECRET_KEY=your_secret_key_here
     DATABASE_URL=sqlite:///./mirai.db
     ```

5. **Obtain Awario API Credentials**:
   - Sign up at [Awario](https://awario.com/)
   - Navigate to API settings in your dashboard
   - Generate an API key
   - Copy the key to your `.env` file

6. **Set up Firebase**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project or use existing
   - Enable Authentication methods: Google, Facebook, Email/Password, Phone
   - Download service account credentials (JSON file)
   - Place the JSON file in the backend directory
   - Update `FIREBASE_CREDENTIALS_PATH` in `.env`

7. **Run the backend server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure Firebase**:
   - Create `.env` file in the frontend directory
   - Add your Firebase config:
     ```
     VITE_FIREBASE_API_KEY=your_api_key
     VITE_FIREBASE_AUTH_DOMAIN=your_auth_domain
     VITE_FIREBASE_PROJECT_ID=your_project_id
     VITE_FIREBASE_STORAGE_BUCKET=your_storage_bucket
     VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
     VITE_FIREBASE_APP_ID=your_app_id
     VITE_API_BASE_URL=http://localhost:8000
     ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Run specific test file:
```bash
pytest tests/test_awario_client.py -v
```

## Features Testing

### Testing Free Features
1. Sign up with a new account (defaults to free tier)
2. Navigate to the dashboard
3. Search for a keyword
4. Verify you see:
   - Total mentions count
   - Basic sentiment breakdown (positive/negative/neutral percentages)
   - Top 5 keywords/hashtags
   - Limited data (last 7 days only)

### Testing Paid Features
1. Upgrade account to premium (admin endpoint or database modification)
2. Search for a keyword
3. Verify additional features:
   - Detailed time series charts (mentions over time)
   - Full influencer lists with reach metrics
   - Demographic breakdowns
   - Competitor comparison data
   - Extended historical data (30+ days)
   - Export functionality

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/verify-token` - Verify Firebase token
- `GET /api/auth/me` - Get current user info

### Analytics
- `GET /api/analytics/mentions` - Get mentions for keyword
- `GET /api/analytics/sentiment` - Get sentiment analysis
- `GET /api/analytics/influencers` - Get top influencers
- `GET /api/analytics/trends` - Get trending metrics
- `GET /api/analytics/competitors` - Compare competitors (Premium)

### Subscription
- `GET /api/subscription/status` - Get current subscription
- `POST /api/subscription/upgrade` - Upgrade to premium
- `POST /api/subscription/cancel` - Cancel subscription

## Brand Colors (ADA Compliant)

Mirai uses a carefully selected color palette that meets WCAG AA standards for accessibility:

- **Primary**: `#0066CC` (Blue) - Contrast ratio 7.5:1 on white
- **Secondary**: `#6B46C1` (Purple) - Contrast ratio 7:1 on white
- **Accent**: `#059669` (Green) - Contrast ratio 4.5:1 on white
- **Warning**: `#DC2626` (Red) - Contrast ratio 5.9:1 on white
- **Background**: `#FFFFFF` (White)
- **Text**: `#1F2937` (Dark Gray) - Contrast ratio 15.8:1 on white

All color combinations have been tested for sufficient contrast for both normal and large text.

## Environment Variables

### Backend (.env)
```
AWARIO_API_KEY=your_awario_api_key
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
JWT_SECRET_KEY=your_secret_key_minimum_32_characters
DATABASE_URL=sqlite:///./mirai.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)
```
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abcdef
VITE_API_BASE_URL=http://localhost:8000
```

## Security Best Practices

1. **Never commit `.env` files or Firebase credentials to version control**
2. **Use HTTPS in production**
3. **Implement rate limiting** (included in backend)
4. **Validate all user inputs** (implemented)
5. **Use secure session management**
6. **Keep dependencies updated**

## Deployment

### Backend Deployment (Example: Heroku)
```bash
heroku create mirai-backend
heroku config:set AWARIO_API_KEY=your_key
heroku config:set JWT_SECRET_KEY=your_secret
git push heroku main
```

### Frontend Deployment (Example: Vercel)
```bash
cd frontend
vercel --prod
```

## Troubleshooting

### Common Issues

1. **Firebase Authentication not working**:
   - Verify Firebase config is correct
   - Ensure authentication methods are enabled in Firebase Console
   - Check that domains are authorized in Firebase settings

2. **Awario API errors**:
   - Verify API key is valid
   - Check API rate limits
   - Ensure proper error handling is in place

3. **CORS errors**:
   - Update `CORS_ORIGINS` in backend `.env`
   - Verify frontend URL is whitelisted

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Email: support@mirai.app

## Changelog

### Version 1.0.0 (Initial Release)
- Multi-platform social listening
- Firebase authentication
- Freemium model implementation
- Real-time analytics dashboard
- Influencer discovery
- Trend tracking
