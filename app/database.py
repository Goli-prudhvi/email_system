# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from config import get_postgres_config

Base = declarative_base()


_engine = None
_SessionLocal = None


def get_engine():
    """Lazy initialization of database engine"""
    global _engine
    
    if _engine is None:
        cfg = get_postgres_config()

        if not all(cfg.values()):
            raise RuntimeError(
                "PostgreSQL environment variables are missing. "
                "Please set POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB."
            )

        password = quote_plus(cfg["password"])

        DATABASE_URL = (
            f"postgresql+psycopg2://{cfg['user']}:{password}"
            f"@{cfg['host']}:{cfg['port']}/{cfg['database']}"
            "?sslmode=require"
        )

        _engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    
    return _engine


def get_session_local():
    """Get sessionmaker, initializing engine if needed"""
    global _SessionLocal
    
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
        )
    
    return _SessionLocal



