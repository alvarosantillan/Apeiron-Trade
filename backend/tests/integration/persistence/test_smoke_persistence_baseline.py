import pytest


@pytest.mark.smoke
def test_smoke_migration_and_crud_baseline(test_client):
    creds = {"email": "smoke@example.com", "password": "Password123"}
    register = test_client.post("/v1/auth/register", json=creds)
    assert register.status_code == 201

    login = test_client.post("/v1/auth/login", json=creds)
    assert login.status_code == 200
    token = login.json()["accessToken"]
    headers = {"Authorization": f"Bearer {token}"}

    providers = test_client.get("/v1/ai-agent/providers", headers=headers)
    assert providers.status_code == 200

    current = test_client.get("/v1/users/me", headers=headers)
    assert current.status_code == 200
    assert current.json()["email"] == creds["email"]
