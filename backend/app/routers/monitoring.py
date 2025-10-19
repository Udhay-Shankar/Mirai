"""
Database monitoring API endpoints.
Provides real-time metrics and health checks.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.monitoring.db_monitor import DatabaseMonitor, SecurityMonitor
from app.auth.jwt_handler import jwt_handler
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/monitor", tags=["Monitoring"])


# Admin dependency (require admin role)
async def require_admin(authorization: Optional[str] = None):
    """Verify user has admin privileges."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    token = authorization.split(" ")[1]
    payload = jwt_handler.decode_token(token)
    
    # Check if user is admin (you'll need to add is_admin field to User model)
    # For now, just verify token is valid
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return payload


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Basic health check endpoint."""
    try:
        # Simple query to test connection
        from sqlalchemy import text
        await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


@router.get("/db/connections")
async def get_connections(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Get current database connection statistics."""
    monitor = DatabaseMonitor(db)
    return await monitor.get_connection_stats()


@router.get("/db/performance")
async def get_performance(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Get query performance metrics."""
    monitor = DatabaseMonitor(db)
    return {
        "query_performance": await monitor.get_query_performance(),
        "cache_hit_ratio": await monitor.get_cache_hit_ratio(),
        "long_running_queries": await monitor.get_long_running_queries()
    }


@router.get("/db/size")
async def get_database_size(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Get database and table sizes."""
    monitor = DatabaseMonitor(db)
    return {
        "database": await monitor.get_database_size(),
        "tables": await monitor.get_table_sizes()
    }


@router.get("/db/indexes")
async def get_index_stats(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Get index usage statistics."""
    monitor = DatabaseMonitor(db)
    return {
        "index_usage": await monitor.get_index_usage(),
        "unused_indexes": await monitor.get_unused_indexes()
    }


@router.get("/db/blocking")
async def get_blocking_queries(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Find queries that are blocking others."""
    monitor = DatabaseMonitor(db)
    return await monitor.get_blocking_queries()


@router.get("/db/vacuum")
async def get_vacuum_stats(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Get vacuum and table bloat statistics."""
    monitor = DatabaseMonitor(db)
    return await monitor.get_vacuum_stats()


@router.get("/db/full-report")
async def get_full_report(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Get comprehensive database health report."""
    monitor = DatabaseMonitor(db)
    return await monitor.get_full_health_report()


@router.get("/security/sessions")
async def get_active_sessions(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Get all active database sessions."""
    monitor = SecurityMonitor(db)
    return await monitor.get_active_sessions()


@router.get("/security/suspicious")
async def detect_suspicious_activity(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Detect suspicious query patterns."""
    monitor = SecurityMonitor(db)
    return await monitor.detect_suspicious_queries()


@router.post("/db/kill-query/{pid}")
async def kill_query(
    pid: int,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Kill a specific database query by PID."""
    try:
        from sqlalchemy import text
        await db.execute(text(f"SELECT pg_terminate_backend({pid})"))
        return {"success": True, "message": f"Terminated connection {pid}"}
    except Exception as e:
        logger.error(f"Error killing query {pid}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to terminate connection: {str(e)}"
        )
