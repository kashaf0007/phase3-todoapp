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
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")