"""
Mirai Backend - FastAPI Application
Main entry point for the social listening API.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import logging
import sys

from app.config import settings
from app.database import init_db
from app.routers import auth_new as auth, analytics, subscription
from app.awario.exceptions import AwarioException

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.debug_mode else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting Mirai API server...")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Mirai API server...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description="Social Listening Platform API powered by Awario",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add SessionMiddleware for OAuth (must be added before CORS)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.jwt_secret_key,  # Use JWT secret for session encryption
    session_cookie="mirai_session",
    max_age=3600,  # 1 hour
    same_site="lax",
    https_only=False  # Set to True in production with HTTPS
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(AwarioException)
async def awario_exception_handler(request: Request, exc: AwarioException):
    """Handle Awario API errors."""
    logger.error(f"Awario API error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": "Social listening service error",
            "message": str(exc)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )


# Include routers
app.include_router(auth.router)
app.include_router(analytics.router)
app.include_router(subscription.router)


# Health check endpoint
@app.get("/health", tags=["Health"])
@limiter.limit("10/minute")
async def health_check(request: Request):
    """
    Health check endpoint.
    
    Returns:
        API health status
    """
    return {
        "status": "healthy",
        "version": settings.api_version,
        "service": "Mirai Social Listening API"
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        Welcome message and API details
    """
    return {
        "message": "Welcome to Mirai Social Listening API",
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/health"
    }


# API info endpoint
@app.get("/api/info", tags=["Info"])
async def api_info():
    """
    Get API information and available endpoints.
    
    Returns:
        API metadata
    """
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "description": "Social Listening Platform powered by Awario",
        "endpoints": {
            "authentication": "/api/auth",
            "analytics": "/api/analytics",
            "subscription": "/api/subscription"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "features": {
            "multi_platform_tracking": True,
            "sentiment_analysis": True,
            "influencer_discovery": True,
            "trend_analysis": True,
            "competitor_comparison": True,
            "freemium_model": True
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug_mode,
        log_level="info" if settings.debug_mode else "warning"
    )
