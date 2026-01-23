"""
Health check endpoint for database connectivity in the Todo application.
This module provides an endpoint to check the health of the database connection.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Dict
from datetime import datetime
import logging

from .database.connection import engine
from .database.deps import get_session
from .models.task import Task

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/health/db")
def db_health_check(session: Session = Depends(get_session)) -> Dict:
    """
    Health check endpoint for database connectivity.
    
    Returns:
        Dict containing health status information
    """
    try:
        # Test the database connection by performing a simple query
        # Using the Task model to check if the table exists and is accessible
        statement = select(Task).limit(1)
        result = session.exec(statement)
        
        # If we get here, the connection is working
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "message": "Database connection is healthy"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "database": "disconnected",
                "error": str(e),
                "message": "Database connection is unhealthy"
            }
        )


@router.get("/health")
def overall_health_check() -> Dict:
    """
    Overall health check endpoint.
    
    Returns:
        Dict containing overall health status information
    """
    # Check if we can connect to the database engine
    try:
        with Session(engine) as session:
            # Perform a simple query to test the connection
            statement = select(Task).limit(1)
            session.exec(statement)
            
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": "connected",
                "api": "responsive"
            },
            "message": "Application is healthy"
        }
    except Exception as e:
        logger.error(f"Overall health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": "disconnected",
                "api": "degraded"
            },
            "error": str(e),
            "message": "Application is unhealthy"
        }