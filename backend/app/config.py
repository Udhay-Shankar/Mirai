"""
Configuration module for Mirai backend.
Loads environment variables and provides application settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    api_version: str = "v1"
    app_name: str = "Mirai Social Listening API"
    debug_mode: bool = True
    
    # Social Media Analysis API
    social_media_api_key: str = "placeholder_key"  # Your social media analysis API key
    
    # Awario API
    awario_api_key: str = "placeholder_key"
    awario_base_url: str = "https://api.awario.com/v1"
    
    # Firebase
    firebase_credentials_path: str = "./firebase-credentials.json"
    
    # JWT
    jwt_secret_key: str = "dev_secret_key_change_in_production_at_least_32_chars_long"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60 * 24  # 24 hours
    access_token_expire_minutes: int = 1440  # 24 hours
    refresh_token_expire_days: int = 30
    
    # OAuth Providers (Optional)
    google_client_id: str = "your_google_client_id"
    google_client_secret: str = "your_google_client_secret"
    facebook_client_id: str = "your_facebook_app_id"
    facebook_client_secret: str = "your_facebook_app_secret"
    twitter_client_id: str = "your_twitter_client_id"
    twitter_client_secret: str = "your_twitter_client_secret"
    instagram_client_id: str = "your_instagram_app_id"
    instagram_client_secret: str = "your_instagram_app_secret"
    
    # Database
    database_url: str = "sqlite:///./mirai.db"
    
    # CORS
    frontend_url: str = "http://localhost:5173"
    cors_origins: str | List[str] = "http://localhost:5173,http://localhost:3000"
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v


# Global settings instance
settings = Settings()

