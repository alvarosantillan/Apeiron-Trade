def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def test_execute_duplicate_request_id_returns_409(test_client):
    headers = _auth_headers(test_client, "trade-exec-dup@example.com")

    payload = {
        "request_id": "req-dup-1",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 10,
        "is_simulation": True,
        "source": "manual",
    }

    first = test_client.post("/v1/trading/execute", json=payload, headers=headers)
    assert first.status_code == 200

    second = test_client.post("/v1/trading/execute", json=payload, headers=headers)
    assert second.status_code == 409
