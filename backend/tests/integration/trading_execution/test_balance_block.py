from services.subscriptions.store import subscription_store


def _auth_headers(test_client, email: str) -> tuple[dict, str]:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    from services.auth.token_service import decode_token

    user_id = decode_token(access_token)["sub"]
    return {"Authorization": f"Bearer {access_token}"}, user_id


def _save_credentials(test_client, headers: dict) -> None:
    test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_balance123", "secret_key": "sec_balance123"},
        headers=headers,
    )


def test_insufficient_balance_is_blocked(test_client):
    headers, user_id = _auth_headers(test_client, "exec-balance@example.com")
    subscription_store.set_status(user_id, "plus", "active")
    _save_credentials(test_client, headers)

    payload = {
        "requestId": "req-balance-1",
        "source": "MANUAL",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 5000,
        "isSimulation": False,
    }
    response = test_client.post("/v1/trading/executions", json=payload, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "BLOCKED"
    assert body["blockedReason"] == "insufficient_balance"
