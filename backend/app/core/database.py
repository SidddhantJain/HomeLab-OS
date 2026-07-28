from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import os

db_url = settings.get_database_url()

# Enable SQLite fallback if testing environment variable is set or postgres fails
if os.getenv("TESTING", "0") == "1" or "sqlite" in db_url:
    engine = create_engine("sqlite:///./homelab_test.db", connect_args={"check_same_thread": False})
else:
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
    except Exception:
        engine = create_engine("sqlite:///./homelab_fallback.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
