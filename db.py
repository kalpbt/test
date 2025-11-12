"""Database initialization and session management.

Uses SQLAlchemy 2.0 style engine and sessionmaker. Reads DATABASE_URL from
environment (and .env via python-dotenv) with a SQLite fallback for local dev.
"""
from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./dev.db"

# echo SQL for debugging when needed
ENGINE = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True)


def get_session() -> Generator:
    """Yield a SQLAlchemy session and ensure it's closed after use.

    Usage (context manager style):
        with get_session() as session:
            ...
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db(Base) -> None:
    """Create database tables for all models that inherit from Base.

    Base should be the declarative base imported from `models`.
    """
    Base.metadata.create_all(bind=ENGINE)
