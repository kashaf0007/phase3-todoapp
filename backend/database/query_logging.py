"""
Database query logging for the Todo application.
This module provides logging functionality for database queries to aid in debugging.
"""

import logging
from functools import wraps
from typing import Any, Callable
from datetime import datetime
import json


# Set up logger for database queries
db_logger = logging.getLogger("database.queries")
db_logger.setLevel(logging.INFO)

# Create file handler for database queries
query_handler = logging.FileHandler("logs/database_queries.log")
query_handler.setLevel(logging.INFO)

# Create console handler for database queries
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter for database queries
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
query_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
db_logger.addHandler(query_handler)
db_logger.addHandler(console_handler)


def log_query(query_func: Callable) -> Callable:
    """
    Decorator to log database queries.
    
    Args:
        query_func: The database query function to wrap
        
    Returns:
        Wrapped function with logging
    """
    @wraps(query_func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        db_logger.info(f"Executing query: {query_func.__name__}")
        db_logger.info(f"Args: {args[1:] if len(args) > 0 else []}")  # Skip 'self' if present
        db_logger.info(f"Kwargs: {kwargs}")
        
        try:
            result = query_func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            db_logger.info(f"Query {query_func.__name__} completed successfully in {duration:.4f}s")
            return result
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            db_logger.error(f"Query {query_func.__name__} failed after {duration:.4f}s: {str(e)}")
            raise
    
    return wrapper


def log_sql_query(sql_statement: str, params: dict = None) -> None:
    """
    Log a raw SQL query.
    
    Args:
        sql_statement: The SQL statement being executed
        params: Parameters passed to the query
    """
    db_logger.info(f"SQL Query: {sql_statement}")
    if params:
        db_logger.info(f"Parameters: {params}")


def setup_query_logging():
    """
    Set up query logging infrastructure.
    This function ensures the logs directory exists and logging is properly configured.
    """
    import os
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Ensure the logger is properly configured
    if not db_logger.handlers:
        db_logger.addHandler(query_handler)
        db_logger.addHandler(console_handler)


# Example usage of logging in service functions
def log_task_operation(operation: str, task_data: dict, user_id: str = None):
    """
    Log task-related operations.
    
    Args:
        operation: The operation being performed (create, update, delete, etc.)
        task_data: The task data involved in the operation
        user_id: The ID of the user performing the operation
    """
    log_entry = {
        "operation": operation,
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "task_data": task_data
    }
    db_logger.info(f"Task Operation: {json.dumps(log_entry, indent=2)}")


def log_user_access(user_id: str, resource: str, action: str):
    """
    Log user access to resources.
    
    Args:
        user_id: The ID of the user accessing the resource
        resource: The resource being accessed
        action: The action being performed
    """
    log_entry = {
        "user_id": user_id,
        "resource": resource,
        "action": action,
        "timestamp": datetime.now().isoformat()
    }
    db_logger.info(f"User Access: {json.dumps(log_entry, indent=2)}")