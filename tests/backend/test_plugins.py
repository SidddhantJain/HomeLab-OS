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


def test_plugin_registration_and_list(client):
    # 1. Register plugin
    reg_resp = client.post("/api/v1/plugins/register", json={
        "plugin_id": "homelab-weather-plugin",
        "name": "Weather Widget Plugin",
        "version": "1.2.0"
    })
    assert reg_resp.status_code == 200
    assert reg_resp.json()["name"] == "Weather Widget Plugin"

    # 2. List plugins
    list_resp = client.get("/api/v1/plugins")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) > 0
