"""
Database Configuration
Neon Serverless PostgreSQL connection and session management.
"""

from typing import Generator
from sqlmodel import Session, create_engine
from sqlalchemy.pool import Pool
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable not set. "
        "Please configure Neon PostgreSQL connection string in .env file."
    )

# Create SQLModel engine with connection pooling
# Neon-specific configuration for serverless PostgreSQL
# For SQLite, we need different connection parameters
if DATABASE_URL.startswith("sqlite"):
    # SQLite-specific configuration
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Set to True for SQL logging in development
        connect_args={"check_same_thread": False},  # Required for SQLite with FastAPI
    )
else:
    # PostgreSQL-specific configuration
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Set to True for SQL logging in development
        pool_pre_ping=True,  # Validate connections before use
        pool_size=5,  # Concurrent connections
        max_overflow=10,  # Additional connections under load
        pool_recycle=300,  # Recycle connections after 5 minutes (Neon serverless)
        connect_args={
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        }
    )


def get_session() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.

    Yields:
        Session: SQLModel database session

    Usage:
        @app.get("/endpoint")
        def endpoint(session: Session = Depends(get_session)):
            # Database operations here
            pass

    Note:
        - Session automatically commits on success
        - Session automatically rolls back on exception
        - Session automatically closes after request
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Create all database tables defined in SQLModel models.

    Call this during application startup to initialize schema.

    Note:
        - Uses SQLModel.metadata.create_all(engine)
        - Only creates tables that don't exist (safe to call multiple times)
        - For production, consider using Alembic migrations instead
    """
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
