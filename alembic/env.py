import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

# add project root to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# import SQLModel metadata
from sqlmodel import SQLModel
try:
    # prefer the async models if present
    from models_async import *  # noqa: F401,F403
    target_metadata = SQLModel.metadata
except Exception:
    # fallback to sync models
    try:
        from models import *  # noqa: F401,F403
        target_metadata = SQLModel.metadata
    except Exception:
        target_metadata = None


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = AsyncEngine(
        None
    )
    # Alembic will normally set a URL in alembic.ini; if not, read from env
    url = config.get_main_option("sqlalchemy.url") or os.getenv("DATABASE_URL")
    if url is None:
        raise RuntimeError("No database URL provided to Alembic (set sqlalchemy.url or DATABASE_URL)")

    from sqlalchemy.ext.asyncio import create_async_engine

    connectable = create_async_engine(url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
