import os
import sys
import pytest

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.core.database import Base, engine, SessionLocal
from app.core.homelab_core import HomelabCore


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_update_sequence_and_history():
    HomelabCore.reset()
    core = HomelabCore.instance()
    core.startup()

    db = SessionLocal()
    try:
        up_svc = core.get_service("updates")
        chk = up_svc.check_update()
        assert chk["update_available"] is True

        rec = up_svc.perform_update(db, "1.1.0")
        assert rec.status in ("COMPLETED", "ROLLED_BACK")
        assert rec.to_version == "1.1.0"
    finally:
        db.close()
        core.shutdown()
