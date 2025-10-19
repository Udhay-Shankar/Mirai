"""
Firebase Authentication integration.
Handles user authentication via Firebase Auth (Google, Facebook, Email, Phone).
"""
import firebase_admin
from firebase_admin import credentials, auth
from app.config import settings
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class FirebaseAuth:
    """Firebase authentication handler."""
    
    def __init__(self):
        """Initialize Firebase Admin SDK."""
        try:
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.firebase_credentials_path)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise
    
    async def verify_token(self, id_token: str) -> Optional[Dict]:
        """
        Verify Firebase ID token.
        
        Args:
            id_token: Firebase ID token from client
            
        Returns:
            Decoded token data if valid, None otherwise
        """
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except auth.InvalidIdTokenError:
            logger.warning("Invalid Firebase ID token")
            return None
        except auth.ExpiredIdTokenError:
            logger.warning("Expired Firebase ID token")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return None
    
    async def get_user(self, uid: str) -> Optional[auth.UserRecord]:
        """
        Get user by Firebase UID.
        
        Args:
            uid: Firebase user ID
            
        Returns:
            UserRecord if found, None otherwise
        """
        try:
            user = auth.get_user(uid)
            return user
        except auth.UserNotFoundError:
            logger.warning(f"User not found: {uid}")
            return None
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None
    
    async def create_custom_token(self, uid: str, claims: Optional[Dict] = None) -> Optional[str]:
        """
        Create custom token for user.
        
        Args:
            uid: Firebase user ID
            claims: Additional claims to include in token
            
        Returns:
            Custom token string if successful, None otherwise
        """
        try:
            token = auth.create_custom_token(uid, claims)
            return token.decode('utf-8')
        except Exception as e:
            logger.error(f"Error creating custom token: {str(e)}")
            return None
    
    async def revoke_refresh_tokens(self, uid: str) -> bool:
        """
        Revoke all refresh tokens for a user.
        
        Args:
            uid: Firebase user ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            auth.revoke_refresh_tokens(uid)
            return True
        except Exception as e:
            logger.error(f"Error revoking tokens: {str(e)}")
            return False


# Global Firebase auth instance
firebase_auth = FirebaseAuth()
