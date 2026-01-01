"""Database connection pool and utilities."""
import logging
from contextlib import contextmanager
from typing import Generator

import mysql.connector
from mysql.connector import pooling
from mysql.connector.pooling import MySQLConnectionPool

from .config import Config

logger = logging.getLogger(__name__)

# Global connection pool
_pool: MySQLConnectionPool = None


def initialize_pool() -> None:
    """Initialize the MySQL connection pool."""
    global _pool
    
    if _pool is not None:
        return
    
    try:
        pool_config = Config.get_db_config()
        pool_config.update({
            'pool_name': Config.POOL_NAME,
            'pool_size': Config.POOL_SIZE,
            'pool_reset_session': True,
        })
        
        _pool = pooling.MySQLConnectionPool(**pool_config)
        logger.info(f"Database connection pool initialized with {Config.POOL_SIZE} connections")
        
    except mysql.connector.Error as err:
        logger.error(f"Failed to initialize connection pool: {err}")
        raise


@contextmanager
def get_connection() -> Generator[mysql.connector.MySQLConnection, None, None]:
    """
    Get a database connection from the pool.
    
    Returns:
        A context manager that yields a database connection.
    
    Raises:
        mysql.connector.Error: If connection cannot be established.
    """
    if _pool is None:
        initialize_pool()
    
    connection = None
    try:
        connection = _pool.get_connection()
        logger.debug("Database connection acquired from pool")
        yield connection
        
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        if connection:
            connection.rollback()
        raise
        
    except Exception as err:
        logger.error(f"Unexpected error: {err}")
        if connection:
            connection.rollback()
        raise
        
    finally:
        if connection and connection.is_connected():
            connection.close()
            logger.debug("Database connection returned to pool")


def close_pool() -> None:
    """Close the connection pool."""
    global _pool
    if _pool:
        logger.info("Closing database connection pool")
        _pool = None