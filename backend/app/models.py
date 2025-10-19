"""
Database models for Mirai application.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()


class SubscriptionTier(str, enum.Enum):
    """Subscription tier enumeration."""
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class User(Base):
    """User model for storing user information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication fields
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=True)  # For email/password auth
    full_name = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    
    # OAuth provider info (email, google, facebook, twitter, instagram)
    provider = Column(String, nullable=False, default="email")
    provider_user_id = Column(String, nullable=True, index=True)  # OAuth provider's user ID
    
    # Legacy fields (for backward compatibility - can be removed after migration)
    firebase_uid = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    display_name = Column(String, nullable=True)  # Deprecated: use full_name
    
    # Subscription information
    subscription_tier = Column(
        SQLEnum(SubscriptionTier),
        default=SubscriptionTier.FREE,
        nullable=False
    )
    subscription_start_date = Column(DateTime, nullable=True)
    subscription_end_date = Column(DateTime, nullable=True)
    
    # Metadata
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, tier={self.subscription_tier})>"
    
    def is_premium(self) -> bool:
        """Check if user has premium access."""
        if self.subscription_tier == SubscriptionTier.FREE:
            return False
        
        # Check if subscription is still valid
        if self.subscription_end_date:
            return datetime.now() < self.subscription_end_date
        
        return True


class Alert(Base):
    """Alert model for storing Awario alerts."""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    awario_alert_id = Column(String, unique=True, index=True, nullable=False)
    
    # Alert configuration
    keyword = Column(String, nullable=False)
    alert_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Alert(id={self.id}, keyword={self.keyword}, user_id={self.user_id})>"
