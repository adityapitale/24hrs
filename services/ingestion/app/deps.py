"""Application dependencies for the ingestion service."""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import AsyncGenerator

from pydantic import BaseSettings, Field
from pydantic_settings import SettingsConfigDict
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Optional redis import kept local to avoid hard dependency when running without Redis.
try:  # pragma: no cover - redis is optional for local skeletons
    from redis.asyncio import Redis  # type: ignore
except ImportError:  # pragma: no cover - redis may not be installed yet
    Redis = None  # type: ignore


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Service configuration loaded from environment variables."""

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/phishguard",
        description="SQLAlchemy database URL.",
    )
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL for caching / Celery broker.",
    )
    celery_broker_url: str = Field(
        default="redis://localhost:6379/1",
        description="Celery broker URL.",
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/1",
        description="Celery result backend URL.",
    )
    gmail_webhook_secret: str = Field(
        default="dev-secret",
        description="Shared secret for verifying Gmail webhook signatures.",
    )
    sql_echo: bool = Field(default=False, description="Enable SQL echo for debugging.")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    settings = Settings()  # type: ignore[call-arg]
    logger.debug("Loaded settings: %s", settings.model_dump())
    return settings


def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Initialise (once) and return the async session factory."""

    global _engine, _session_factory

    if _engine is None or _session_factory is None:
        settings = get_settings()
        _engine = create_async_engine(settings.database_url, echo=settings.sql_echo)
        _session_factory = async_sessionmaker(_engine, expire_on_commit=False)
        logger.info("Initialised database engine for %s", settings.database_url)

    return _session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for request scope."""

    session_factory = _get_session_factory()
    async with session_factory() as session:
        yield session


async def get_redis() -> Redis | None:  # type: ignore[override]
    """Return a Redis client instance (stub for local development)."""

    settings = get_settings()

    if Redis is None:
        logger.warning("redis library not installed; returning None from get_redis stub")
        return None

    # TODO: harden connection pooling and error handling for production use.
    return Redis.from_url(settings.redis_url)

