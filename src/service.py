"""Service layer for business logic."""
import logging
from typing import Dict, Optional, Any

from .repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related business operations."""
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a user by ID.
        
        Args:
            user_id: The user ID to retrieve.
            
        Returns:
            Dictionary containing user data if found, None otherwise.
            
        Raises:
            Exception: If database operation fails.
        """
        try:
            logger.info(f"Fetching user with ID: {user_id}")
            user = self.user_repository.get_user_by_id(user_id)
            
            if user is None:
                logger.info(f"User not found with ID: {user_id}")
                return None
                
            logger.info(f"Successfully retrieved user with ID: {user_id}")
            return user
            
        except Exception as err:
            logger.error(f"Error in user service while fetching user {user_id}: {err}")
            raise


# Global service instance
user_service = UserService()