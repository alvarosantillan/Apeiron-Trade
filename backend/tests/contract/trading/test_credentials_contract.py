def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def test_save_credentials_requires_auth(test_client):
    response = test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_valid123", "secret_key": "sec_valid123"},
    )
    assert response.status_code == 401


def test_save_credentials_returns_200_and_active_status(test_client):
    headers = _auth_headers(test_client, "trade-contract@example.com")

    save = test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_valid123", "secret_key": "sec_valid123"},
        headers=headers,
    )
    assert save.status_code == 200

    status = test_client.get("/v1/trading/binance/credentials/status", headers=headers)
    assert status.status_code == 200
    body = status.json()
    assert body["active"] is True
    assert body["api_key_suffix"] == "d123"
