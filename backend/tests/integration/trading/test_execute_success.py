def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def _save_credentials(test_client, headers: dict) -> None:
    response = test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_live12345", "secret_key": "sec_live12345"},
        headers=headers,
    )
    assert response.status_code == 200


def test_execute_real_buy_order_success(test_client):
    headers = _auth_headers(test_client, "trade-success@example.com")
    _save_credentials(test_client, headers)

    payload = {
        "request_id": "req-success-1",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 100,
        "is_simulation": False,
        "source": "manual",
    }

    response = test_client.post("/v1/trading/execute", json=payload, headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "executed"
    assert body["execution_type"] == "REAL"
