# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from config import get_postgres_config

Base = declarative_base()


def create_db_engine():
    cfg = get_postgres_config()

    if not all(cfg.values()):
        raise RuntimeError("PostgreSQL environment variables are missing")

    password = quote_plus(cfg["password"])

    DATABASE_URL = (
        f"postgresql+psycopg2://{cfg['user']}:{password}"
        f"@{cfg['host']}:{cfg['port']}/{cfg['database']}"
        "?sslmode=require"
    )

    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


engine = create_db_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)



