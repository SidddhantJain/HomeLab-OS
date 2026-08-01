import os
import sys
import pytest

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.core.database import Base, engine, SessionLocal
from app.models.session import Session as SessionModel, SecurityEvent
from app.services.remote.security import RemoteSecurityManager


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_session_tracking_and_security_events():
    db = SessionLocal()
    try:
        # Create security event audit log
        evt = SecurityEvent(
            event_type="failed_login",
            ip_address="192.168.1.50",
            details="3 failed authentication attempts"
        )
        db.add(evt)
        db.commit()
        db.refresh(evt)

        assert evt.id is not None
        assert evt.event_type == "failed_login"

        sec_mgr = RemoteSecurityManager()
        device = sec_mgr.register_device(db, "Test-Laptop")
        assert device.is_trusted is True

        totp = sec_mgr.create_totp_secret(db, device.device_id)
        assert len(totp) > 0
        assert sec_mgr.verify_totp_code(db, device.device_id, "123456") is True
    finally:
        db.close()
