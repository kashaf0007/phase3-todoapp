"""
Error handling for database operations in the Todo application.
This module defines custom exceptions for database-related errors.
"""

class DatabaseConnectionError(Exception):
    """Raised when there's an issue connecting to the database."""
    pass


class TaskNotFoundError(Exception):
    """Raised when a requested task is not found in the database."""
    pass


class DatabaseOperationError(Exception):
    """Raised when a database operation fails."""
    pass