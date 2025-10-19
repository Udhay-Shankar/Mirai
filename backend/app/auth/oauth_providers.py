"""
OAuth provider configurations for social login.
Supports: Google, Facebook, Twitter/X, Instagram
"""
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os

# Initialize OAuth
oauth = OAuth()

# Google OAuth
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Facebook OAuth
oauth.register(
    name='facebook',
    client_id=os.getenv('FACEBOOK_CLIENT_ID'),
    client_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
    authorize_url='https://www.facebook.com/v12.0/dialog/oauth',
    authorize_params=None,
    access_token_url='https://graph.facebook.com/v12.0/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=None,
    client_kwargs={
        'scope': 'email public_profile'
    },
)

# Twitter/X OAuth 2.0
oauth.register(
    name='twitter',
    client_id=os.getenv('TWITTER_CLIENT_ID'),
    client_secret=os.getenv('TWITTER_CLIENT_SECRET'),
    api_base_url='https://api.twitter.com/2/',
    authorize_url='https://twitter.com/i/oauth2/authorize',
    access_token_url='https://api.twitter.com/2/oauth2/token',
    client_kwargs={
        'scope': 'tweet.read users.read',
        'code_challenge_method': 'S256'
    }
)

# Instagram OAuth (via Facebook Graph API)
oauth.register(
    name='instagram',
    client_id=os.getenv('INSTAGRAM_CLIENT_ID'),
    client_secret=os.getenv('INSTAGRAM_CLIENT_SECRET'),
    authorize_url='https://api.instagram.com/oauth/authorize',
    access_token_url='https://api.instagram.com/oauth/access_token',
    client_kwargs={
        'scope': 'user_profile,user_media'
    }
)
