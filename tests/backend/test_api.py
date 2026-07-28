import os
import sys

os.environ["TESTING"] = "1"

import pytest
from fastapi.testclient import TestClient

# Include backend path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import app
from app.core.database import Base, engine

@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "HomeLab OS"
    assert data["version"] == "v1.0"
    assert data["status"] == "running"


def test_auth_register_and_login():
    # Test Registration
    reg_payload = {
        "username": "admin_test",
        "password": "SecretPassword123!",
        "email": "admin@homelab.com",
        "role": "admin"
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["username"] == "admin_test"
    assert user_data["role"] == "admin"

    # Test Duplicate Registration Failure
    dup_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert dup_res.status_code == 400

    # Test Login
    login_payload = {
        "username": "admin_test",
        "password": "SecretPassword123!"
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    assert token_data["username"] == "admin_test"


def test_system_status():
    response = client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "server_name" in data
    assert "cpu" in data
    assert "ram" in data
