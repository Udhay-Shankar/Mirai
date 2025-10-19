"""
Database setup and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings
from app.models import Base
import logging

logger = logging.getLogger(__name__)

# Convert sqlite URL to async if needed
database_url = settings.database_url
if database_url.startswith("sqlite:///"):
    async_database_url = database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    async_database_url = database_url

# Create async engine
engine = create_async_engine(
    async_database_url,
    echo=settings.debug_mode,
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully")


async def get_db() -> AsyncSession:
    """
    Dependency for getting database sessions.
    Yields an async session and ensures proper cleanup.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
