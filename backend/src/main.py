"""
FastAPI Application
Main application initialization and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import get_settings
from .database import create_db_and_tables
from .api.routes import health, tasks, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup: Create database tables (skip if tables already exist)
    print("Checking database tables...")
    try:
        create_db_and_tables()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Table creation skipped (tables may already exist): {e}")
        print("Continuing with existing database schema...")

    yield

    # Shutdown: Cleanup if needed
    print("Shutting down application...")


# Get application settings
settings = get_settings()

# Initialize FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(tasks.router, tags=["Tasks"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Phase II Todo Application API",
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/health"
    }
