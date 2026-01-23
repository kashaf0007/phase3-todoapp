"""
Database connection utility for the Todo application.
This module manages the connection to the Neon PostgreSQL database.
"""

from sqlmodel import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging