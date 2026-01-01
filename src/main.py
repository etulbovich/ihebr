"""Main FastAPI application."""
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import mysql.connector

from .db import initialize_pool, close_pool
from .service import user_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    logger.info("Starting TiDB Reader Service")
    try:
        initialize_pool()
        logger.info("Application startup completed")
    except Exception as err:
        logger.error(f"Failed to start application: {err}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down TiDB Reader Service")
    close_pool()
    logger.info("Application shutdown completed")


# Create FastAPI application
app = FastAPI(
    title="TiDB Reader Service",
    description="A read-only REST API for TiDB users table",
    version="1.0.0",
    openapi_version="3.0.3",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "TiDB Reader Service is running"}


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> Dict[str, Any]:
    """
    Get a user by ID.
    
    Args:
        user_id: The user ID to retrieve.
        
    Returns:
        User data as a JSON object.
        
    Raises:
        HTTPException: 404 if user not found, 500 if database error occurs.
    """
    try:
        user = user_service.get_user_by_id(user_id)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        return user
        
    except mysql.connector.Error as err:
        logger.error(f"Database error while fetching user {user_id}: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as err:
        logger.error(f"Unexpected error while fetching user {user_id}: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler to ensure no secrets are leaked."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )