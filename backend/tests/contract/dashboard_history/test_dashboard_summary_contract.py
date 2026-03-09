def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    return {"Authorization": f"Bearer {login.json()['accessToken']}"}


def test_dashboard_summary_contract(test_client):
    headers = _auth_headers(test_client, "dash-summary@example.com")
    response = test_client.get("/v1/dashboard/summary", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert "planCode" in body
    assert "operationsUsed" in body
    assert "operationsLimit" in body
    assert body["botStatus"] in {"ACTIVE", "PAUSED", "INACTIVE"}
