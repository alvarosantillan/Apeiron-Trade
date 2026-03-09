def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    return {"Authorization": f"Bearer {login.json()['accessToken']}"}


def test_kpi_endpoint_contract(test_client):
    headers = _auth_headers(test_client, "kpi-contract@example.com")
    response = test_client.get("/v1/dashboard/kpis?window=7d", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["window"] == "7d"
    assert "totalTrades" in body


def test_kpi_invalid_window_returns_400(test_client):
    headers = _auth_headers(test_client, "kpi-contract-2@example.com")
    response = test_client.get("/v1/dashboard/kpis?window=90d", headers=headers)
    assert response.status_code == 400
