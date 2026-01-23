"""
Secure connection string parsing for the Todo application.
This module handles parsing and validating database connection strings.
"""

import os
import re
from urllib.parse import urlparse
from typing import Dict, Optional


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parses a PostgreSQL connection string into its components.
    
    Args:
        connection_string: The full connection string
        
    Returns:
        Dictionary containing the parsed components
    """
    if not connection_string.startswith('postgresql://'):
        raise ValueError("Connection string must start with 'postgresql://'")
    
    # Parse the connection string
    parsed = urlparse(connection_string)
    
    # Extract components
    components = {
        'driver': parsed.scheme,
        'username': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': str(parsed.port) if parsed.port else '',
        'database': parsed.path.lstrip('/')
    }
    
    return components


def validate_connection_components(components: Dict[str, str]) -> bool:
    """
    Validates the components of a database connection string.
    
    Args:
        components: Dictionary containing the parsed connection components
        
    Returns:
        True if all required components are valid, False otherwise
    """
    required_fields = ['username', 'password', 'host', 'database']
    
    for field in required_fields:
        if not components.get(field):
            return False
    
    # Validate host format
    host = components['host']
    if not re.match(r'^[\w\.-]+$', host):
        return False
    
    # Validate port if provided
    port = components['port']
    if port and not port.isdigit():
        return False
    
    return True


def get_secure_connection_info() -> Dict[str, str]:
    """
    Gets and parses the database connection string from environment variables.
    
    Returns:
        Dictionary containing the parsed connection components
    """
    connection_string = os.getenv("DATABASE_URL")
    
    if not connection_string:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    components = parse_connection_string(connection_string)
    
    if not validate_connection_components(components):
        raise ValueError("Invalid connection string components")
    
    # Return components without the password for security
    safe_components = components.copy()
    safe_components['password'] = '****'  # Mask the password
    
    return safe_components