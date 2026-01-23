"""
Database session management utilities for the Todo application.
This module provides database session dependencies for FastAPI.
"""

from sqlmodel import Session
from .connection import engine


def get_session():
    """
    Generator function that provides database sessions.
    This function is meant to be used as a FastAPI dependency.
    """
    with Session(engine) as session:
        yield session