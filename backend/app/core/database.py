from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import os

db_url = settings.get_database_url()

# Enable SQLite fallback if testing environment variable is set, or if running bare-metal without Postgres container
if os.getenv("TESTING", "0") == "1" or "sqlite" in db_url:
    engine = create_engine("sqlite:///./homelab_test.db", connect_args={"check_same_thread": False})
else:
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        # Test connection immediately
        with engine.connect() as conn:
            pass
    except Exception:
        # Fallback to local SQLite for bare-metal / standalone execution
        engine = create_engine("sqlite:///./homelab_fallback.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
