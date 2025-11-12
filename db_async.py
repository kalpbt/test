"""Async DB helpers using SQLModel + SQLAlchemy async engine.

This provides an AsyncEngine and an async session generator suitable for FastAPI
dependencies (Depends). DATABASE_URL is read from environment or `.env` and
falls back to a local SQLite file (which will use synchronous mode unless you
use aiosqlite; for production use Postgres with asyncpg).
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Prefer an async Postgres URL. For psycopg v3 and asyncpg driver use:
# postgresql+asyncpg://user:pass@host/dbname
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite+aiosqlite:///./dev_async.db"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def init_db() -> None:
    """Create database tables using SQLModel metadata.

    Use inside an async entrypoint (e.g. startup event in FastAPI) or via an
    async script.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async SQLModel/SQLAlchemy session.

    Use as a FastAPI dependency: `Depends(get_session)`
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
