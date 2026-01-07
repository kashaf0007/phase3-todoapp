"""
Health Check Endpoint
Simple endpoint to verify API is running.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status message indicating API is healthy

    Example:
        GET /health
        Response: {"status": "healthy"}
    """
    return {"status": "healthy"}
