from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.settings import Settings

Base = declarative_base()

_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def init_db(settings: Settings):
    """Initialize SQLAlchemy engine and sessionmaker with provided settings."""
    global _engine, _SessionLocal

    _engine = create_engine(settings.database_url)
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine, _SessionLocal


def get_db():
    """Dependency for FastAPI. Requires init_db() to be called before use."""
    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db(settings) first.")

    db: Session = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
