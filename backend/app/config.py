"""
Environment variables handling with python-dotenv
"""
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database configuration - Use DATABASE_URL from .env file
NEON_DATABASE_URL = os.getenv("DATABASE_URL")

# Authentication configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Security configuration
DOMAIN_ALLOWLIST = os.getenv("DOMAIN_ALLOWLIST", "").split(",")

# Application configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")