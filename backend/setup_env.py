"""
Secure API Key Setup Script
DO NOT share this file with your API keys filled in!
"""
import os
from pathlib import Path


def setup_env_file():
    """Create .env file with secure configuration."""
    
    backend_dir = Path(__file__).parent
    env_file = backend_dir / '.env'
    
    # Check if .env already exists
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted. Keeping existing .env file.")
            return
    
    print("🔐 Secure API Key Setup")
    print("=" * 50)
    print("\n⚠️  SECURITY REMINDERS:")
    print("   • Never commit .env to Git")
    print("   • Never share API keys publicly")
    print("   • Keep this information secure")
    print("   • Use different keys for dev/prod")
    print("\n" + "=" * 50 + "\n")
    
    # Collect API keys securely
    print("📝 Enter your API keys (or press Enter to skip):\n")
    
    social_media_api_key = input("Social Media Analysis API Key: ").strip()
    if not social_media_api_key:
        social_media_api_key = "your_social_media_api_key_here"
    
    awario_api_key = input("Awario API Key (optional): ").strip()
    if not awario_api_key:
        awario_api_key = "your_awario_api_key_here"
    
    # Generate JWT secret if needed
    import secrets
    jwt_secret = secrets.token_urlsafe(32)
    print(f"\n✅ Generated JWT Secret Key: {jwt_secret[:20]}...")
    
    # OAuth keys
    print("\n🔑 OAuth Provider Keys (optional, press Enter to skip):\n")
    
    google_client_id = input("Google Client ID: ").strip() or "your_google_client_id"
    google_client_secret = input("Google Client Secret: ").strip() or "your_google_client_secret"
    
    facebook_client_id = input("Facebook App ID: ").strip() or "your_facebook_app_id"
    facebook_client_secret = input("Facebook App Secret: ").strip() or "your_facebook_app_secret"
    
    twitter_client_id = input("Twitter Client ID: ").strip() or "your_twitter_client_id"
    twitter_client_secret = input("Twitter Client Secret: ").strip() or "your_twitter_client_secret"
    
    # Database URL
    print("\n💾 Database Configuration:\n")
    print("1. SQLite (Development) - sqlite:///./mirai.db")
    print("2. PostgreSQL (Production) - postgresql://user:pass@host/db")
    
    db_choice = input("\nChoice (1 or 2, default=1): ").strip()
    
    if db_choice == "2":
        db_url = input("PostgreSQL URL: ").strip()
    else:
        db_url = "sqlite:///./mirai.db"
    
    # Create .env content
    env_content = f"""# ⚠️ SECURITY WARNING ⚠️
# NEVER commit this file to Git!
# NEVER share the contents of this file!

# ==============================================
# Social Media Analysis API
# ==============================================
SOCIAL_MEDIA_API_KEY={social_media_api_key}

# ==============================================
# Awario API (Optional)
# ==============================================
AWARIO_API_KEY={awario_api_key}
AWARIO_BASE_URL=https://api.awario.com/v1

# ==============================================
# JWT Authentication
# ==============================================
JWT_SECRET_KEY={jwt_secret}
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=30

# ==============================================
# OAuth Providers
# ==============================================
# Google OAuth
GOOGLE_CLIENT_ID={google_client_id}
GOOGLE_CLIENT_SECRET={google_client_secret}

# Facebook OAuth
FACEBOOK_CLIENT_ID={facebook_client_id}
FACEBOOK_CLIENT_SECRET={facebook_client_secret}

# Twitter OAuth
TWITTER_CLIENT_ID={twitter_client_id}
TWITTER_CLIENT_SECRET={twitter_client_secret}

# Instagram OAuth (uses Facebook credentials)
INSTAGRAM_CLIENT_ID={facebook_client_id}
INSTAGRAM_CLIENT_SECRET={facebook_client_secret}

# ==============================================
# Database
# ==============================================
DATABASE_URL={db_url}

# ==============================================
# Application Settings
# ==============================================
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
API_VERSION=v1
DEBUG_MODE=True
RATE_LIMIT_PER_MINUTE=60
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100

# ==============================================
# Firebase (Legacy - Optional)
# ==============================================
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
"""
    
    # Write to file
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("\n✅ .env file created successfully!")
    print(f"📁 Location: {env_file.absolute()}")
    
    # Verify .gitignore
    gitignore_file = backend_dir.parent / '.gitignore'
    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            content = f.read()
            if '.env' not in content:
                print("\n⚠️  WARNING: .env is NOT in .gitignore!")
                print("   Add '.env' to your .gitignore file immediately!")
            else:
                print("✅ .env is protected by .gitignore")
    
    print("\n" + "=" * 50)
    print("🔒 SECURITY CHECKLIST:")
    print("   [✓] .env file created")
    print("   [✓] JWT secret generated")
    print("   [ ] Verify .env is in .gitignore")
    print("   [ ] Never commit .env to Git")
    print("   [ ] Use different keys for production")
    print("=" * 50)


if __name__ == "__main__":
    try:
        setup_env_file()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
