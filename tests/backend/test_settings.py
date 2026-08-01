import os
import sys
import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import app
from app.core.database import Base, engine
from app.core.homelab_core import HomelabCore


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    HomelabCore.reset()
    with TestClient(app) as c:
        yield c


def test_settings_get_and_update(client):
    # 1. Get
    resp = client.get("/api/v1/settings")
    assert resp.status_code == 200
    st = resp.json()
    assert st["theme"] == "dark"

    # 2. Update
    up_resp = client.put("/api/v1/settings", json={"theme": "light", "language": "es"})
    assert up_resp.status_code == 200
    assert up_resp.json()["theme"] == "light"
    assert up_resp.json()["language"] == "es"
