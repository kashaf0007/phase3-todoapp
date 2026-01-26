"""
Global exception handlers for the application
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from ..utils.exceptions import BaseAppException, ResourceNotFoundException, UnauthorizedAccessException, InvalidParametersException
from typing import Union
import logging

logger = logging.getLogger(__name__)

async def handle_base_app_exception(request: Request, exc: BaseAppException):
    """
    Handle custom application exceptions
    """
    logger.error(f"Application error: {exc.message} (Code: {exc.error_code})")
    
    if isinstance(exc, ResourceNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": {
                    "type": exc.error_code,
                    "message": exc.message
                }
            }
        )
    elif isinstance(exc, UnauthorizedAccessException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": {
                    "type": exc.error_code,
                    "message": exc.message
                }
            }
        )
    elif isinstance(exc, InvalidParametersException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": {
                    "type": exc.error_code,
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "type": "INTERNAL_ERROR",
                    "message": "An internal error occurred"
                }
            }
        )

async def handle_http_exception(request: Request, exc):
    """
    Handle HTTP exceptions
    """
    logger.warning(f"HTTP error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "HTTP_ERROR",
                "message": str(exc.detail)
            }
        }
    )

async def handle_general_exception(request: Request, exc: Exception):
    """
    Handle general exceptions
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "type": "INTERNAL_ERROR",
                "message": "An internal server error occurred"
            }
        }
    )