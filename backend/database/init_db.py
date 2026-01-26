"""
Database initialization module for the Todo application.
This module handles the creation of database tables.
"""

from sqlmodel import SQLModel
from .connection import engine


def create_db_and_tables():
    """
    Creates all database tables based on SQLModel definitions.
    This function should be called when the application starts.
    """
    # Clear the existing metadata to avoid conflicts
    SQLModel.metadata.clear()

    # Import models to register them with the metadata
    # Import from the app directory to avoid conflicts
    from ..app.models.task import Task
    from ..app.models.conversation import Conversation
    from ..app.models.message import Message

    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")