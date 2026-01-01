"""Repository layer for user data access."""
import logging
from typing import Dict, Optional, Any

import mysql.connector

from .db import get_connection

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository class for user data operations."""
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by ID.
        
        Args:
            user_id: The user ID to search for.
            
        Returns:
            Dictionary containing user data if found, None otherwise.
            
        Raises:
            mysql.connector.Error: If database operation fails.
        """
        query = "SELECT * FROM users WHERE id = %s"
        
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (user_id,))
                
                # Get column names from cursor description
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                
                # Fetch the row
                row = cursor.fetchone()
                cursor.close()
                
                if row is None:
                    logger.debug(f"No user found with ID: {user_id}")
                    return None
                
                # Convert row tuple to dictionary using column names
                user_data = dict(zip(columns, row))
                logger.debug(f"User found with ID: {user_id}")
                return user_data
                
        except mysql.connector.Error as err:
            logger.error(f"Database error while fetching user {user_id}: {err}")
            raise
        except Exception as err:
            logger.error(f"Unexpected error while fetching user {user_id}: {err}")
            raise