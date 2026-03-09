def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def test_invalid_binance_credentials_return_400(test_client):
    headers = _auth_headers(test_client, "trade-invalid@example.com")
    response = test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bad", "secret_key": "wrong"},
        headers=headers,
    )

    assert response.status_code == 400


def test_status_without_credentials_is_inactive(test_client):
    headers = _auth_headers(test_client, "trade-empty@example.com")
    response = test_client.get("/v1/trading/binance/credentials/status", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["active"] is False
    assert body["api_key_suffix"] is None
