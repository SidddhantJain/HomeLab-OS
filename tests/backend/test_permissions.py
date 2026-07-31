import os
import sys
import pytest

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.core.database import Base, engine, SessionLocal
from app.core.homelab_core import HomelabCore
from app.core.permissions import PermissionModel, SystemRole, ActionType


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_permission_evaluations():
    # Make sure core is initialized for event publishing
    HomelabCore.reset()
    core = HomelabCore.instance()
    core.startup()

    db = SessionLocal()
    try:
        # Verify seeding
        PermissionModel.initialize_default_roles_and_permissions(db)

        # ADMIN should have storage write permission
        allowed_admin = PermissionModel.check_permission(db, "test_admin", SystemRole.ADMIN.value, "storage", ActionType.WRITE.value)
        assert allowed_admin is True

        # GUEST should NOT have storage write permission
        allowed_guest = PermissionModel.check_permission(db, "test_guest", SystemRole.GUEST.value, "storage", ActionType.WRITE.value)
        assert allowed_guest is False

    finally:
        db.close()
        core.shutdown()
