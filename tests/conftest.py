import sys
import os

# Set TESTING environment variable before importing any app modules
os.environ["TESTING"] = "1"

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
backend_dir = os.path.join(root_dir, "backend")

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Remove any stale test database file before initializing
for db_file in ["homelab_test.db", "homelab.db"]:
    db_path = os.path.join(root_dir, db_file)
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

# Import models and create all database tables for test session
from app.core.database import Base, engine
import app.models  # Ensures all SQLAlchemy models are registered

Base.metadata.create_all(bind=engine)



