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


def test_power_management_endpoints(client):
    # 1. Report
    rep_resp = client.get("/api/v1/power/report")
    assert rep_resp.status_code == 200
    assert rep_resp.json()["power_state"] == "AC_CONNECTED"

    # 2. Schedule create
    sched_resp = client.post("/api/v1/power/schedules", json={
        "name": "Nightly Sleep",
        "action": "sleep",
        "cron_expression": "0 0 * * *"
    })
    assert sched_resp.status_code == 200
    assert sched_resp.json()["name"] == "Nightly Sleep"

    # 3. List schedules
    list_resp = client.get("/api/v1/power/schedules")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) > 0

    # 4. Wakeup packet
    wol_resp = client.post("/api/v1/power/wakeup")
    assert wol_resp.status_code == 200

    # 5. Remote shutdown requirement check
    bad_sd = client.post("/api/v1/power/shutdown?confirmation=NO")
    assert bad_sd.status_code == 400

    good_sd = client.post("/api/v1/power/shutdown?confirmation=SHUTDOWN")
    assert good_sd.status_code == 200
