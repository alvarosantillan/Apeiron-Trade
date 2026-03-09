import pytest


@pytest.mark.runtime
def test_runtime_continuity_openapi_invariants(test_client):
    response = test_client.get("/openapi.json")

    assert response.status_code == 200
    payload = response.json()
    paths = payload.get("paths", {})

    assert "/v1/auth/login" in paths
    assert "/v1/auth/register" in paths
    assert "/v1/users/me" in paths
