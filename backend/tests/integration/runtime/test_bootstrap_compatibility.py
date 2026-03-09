import os

from fastapi.testclient import TestClient
import pytest

from main import app


@pytest.mark.runtime
@pytest.mark.runtime_warning_policy
def test_bootstrap_compatibility_across_client_restart(test_client):
    creds = {"email": "runtime-compat@example.com", "password": "Password123"}
    register = test_client.post("/v1/auth/register", json=creds)
    assert register.status_code == 201

    with TestClient(app) as restarted_client:
        login = restarted_client.post("/v1/auth/login", json=creds)
        assert login.status_code == 200

    assert os.environ["DATABASE_URL"].startswith("sqlite:///")
