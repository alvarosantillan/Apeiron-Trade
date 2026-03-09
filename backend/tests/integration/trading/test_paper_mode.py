def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def _save_credentials(test_client, headers: dict) -> None:
    response = test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_mode12345", "secret_key": "sec_mode12345"},
        headers=headers,
    )
    assert response.status_code == 200


def test_paper_execution_does_not_consume_real_weekly_limit(test_client):
    headers = _auth_headers(test_client, "trade-paper@example.com")
    _save_credentials(test_client, headers)

    real_payload = {
        "request_id": "req-real-1",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 100,
        "is_simulation": False,
        "source": "manual",
    }

    first_real = test_client.post("/v1/trading/execute", json=real_payload, headers=headers)
    assert first_real.status_code == 200
    assert first_real.json()["status"] == "executed"

    second_real = dict(real_payload)
    second_real["request_id"] = "req-real-2"
    blocked = test_client.post("/v1/trading/execute", json=second_real, headers=headers)
    assert blocked.status_code == 403
    assert blocked.json()["detail"] == "weekly_limit_exceeded"

    paper_payload = {
        "request_id": "req-paper-1",
        "symbol": "ETHUSDT",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 500,
        "is_simulation": True,
        "source": "manual",
    }
    paper = test_client.post("/v1/trading/execute", json=paper_payload, headers=headers)
    assert paper.status_code == 200
    body = paper.json()
    assert body["execution_type"] == "PAPER"
    assert body["status"] == "executed"
