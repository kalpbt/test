ProcureMind — PostgreSQL integration and ORM models

This repository contains a minimal Python project with SQLAlchemy ORM models and a small DB wiring for the ProcureMind presentation flow (Projects, BOQ items, rate cache, vendors, RFQs, quotes, and agent runs).

Quickstart (Windows PowerShell)

1) Install runtime dependencies in your environment:

```powershell
python -m pip install --upgrade pip
pip install SQLAlchemy psycopg[binary] python-dotenv alembic
```

2) Configure your database URL (Postgres) in an environment variable or create a `.env` file in the project root with:

```text
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/your_db
```

If `DATABASE_URL` is not set, the code will use a local SQLite file `dev.db` for convenience.

3) Run the demo script (creates tables and inserts a sample project + BOQ item):

```powershell
python main.py
```

Files added

- `db.py` — SQLAlchemy engine, sessionmaker, and `init_db` helper.
- `models.py` — ORM models for Project, BOQItem, RateSource, RateCache, Vendor, RFQ, Quote, AgentRun, ClarificationQuestion.
- `main.py` — updated to initialize DB and insert a small demo record.

Next steps

- Run migrations with Alembic (recommended):

1) Configure `alembic.ini` or set `DATABASE_URL` environment variable. Example (PowerShell):

```powershell
$env:DATABASE_URL = 'postgresql+asyncpg://myuser:mypassword@localhost:5432/procuremind'
```

2) Install Alembic (already listed in dependencies) and run:

```powershell
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

The repo includes a minimal `alembic` directory with an `env.py` that uses `sqlmodel.SQLModel.metadata` as the target metadata when `models_async.py` is present.

- Add repository-level services for scraping/ingestion, rate normalization, and agent orchestration.
- Expand tests and CI to validate models and basic queries.
- Add repository-level services for scraping/ingestion, rate normalization, and agent orchestration.
- Expand tests and CI to validate models and basic queries.

