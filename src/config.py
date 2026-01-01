"""Configuration module for TiDB reader service."""
import os
from typing import Optional


class Config:
    """Configuration class for database and application settings."""
    
    # Database configuration from environment variables
    TIDB_HOST: str = os.getenv('TIDB_HOST', 'gateway01.eu-central-1.prod.aws.tidbcloud.com')
    TIDB_PORT: int = int(os.getenv('TIDB_PORT', '4000'))
    TIDB_USER: str = os.getenv('TIDB_USER', '26eB9QM5vtHUGUj.gpt_reader')
    TIDB_PASSWORD: str = os.getenv('TIDB_PASSWORD', 'QAZ2wsx')
    TIDB_DATABASE: str = os.getenv('TIDB_DATABASE', 'IHEBR01')
    TIDB_SSL_MODE: str = os.getenv('TIDB_SSL_MODE', 'PREFERRED')
    
    # Connection pool configuration
    POOL_NAME: str = 'tidb_pool'
    POOL_SIZE: int = int(os.getenv('POOL_SIZE', '10'))
    MAX_OVERFLOW: int = int(os.getenv('MAX_OVERFLOW', '20'))
    
    @classmethod
    def get_db_config(cls) -> dict:
        """Get database connection configuration."""
        return {
            'host': cls.TIDB_HOST,
            'port': cls.TIDB_PORT,
            'user': cls.TIDB_USER,
            'password': cls.TIDB_PASSWORD,
            'database': cls.TIDB_DATABASE,
            'ssl_mode': cls.TIDB_SSL_MODE,
            'autocommit': True,
            'charset': 'utf8mb4',
            'use_unicode': True,
        }