"""
SQLAlchemy engine + session setup for PostgreSQL.

Works with any standard Postgres connection string, including the ones
provided by Supabase and Neon. See `.env.example` for the format.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

connect_args = {}
engine_kwargs = {"pool_pre_ping": True}

# Neon / Supabase sit behind a pooled connection by default; sslmode is
# typically already embedded in their connection strings, so we don't force
# anything here. For local Postgres this just works without extra args.
engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
