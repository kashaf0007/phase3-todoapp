"""
Database configuration validation for the Todo application.
This module validates database configuration settings.
"""

import os
import re
from typing import Optional


def validate_database_url(database_url: Optional[str]) -> bool:
    """
    Validates the format of a database URL.
    
    Args:
        database_url: The database URL to validate
        
    Returns:
        True if the URL is valid, False otherwise
    """
    if not database_url:
        return False
    
    # Regex pattern for PostgreSQL connection string
    pattern = r'^postgresql://[a-zA-Z0-9_-]+:[^@]+@[\w\.-]+:\d+/\w+$'
    
    return bool(re.match(pattern, database_url))


def get_database_config():
    """
    Retrieves and validates database configuration from environment variables.
    
    Returns:
        Dictionary containing database configuration
    """
    database_url = os.getenv("DATABASE_URL")
    
    if not validate_database_url(database_url):
        raise ValueError("Invalid DATABASE_URL format")
    
    return {
        "database_url": database_url
    }


def validate_db_connection():
    """
    Performs basic validation of database connection settings.
    
    Returns:
        True if validation passes, raises exception otherwise
    """
    config = get_database_config()
    
    # Additional validation could be performed here
    # For now, we just validate the format
    
    return True