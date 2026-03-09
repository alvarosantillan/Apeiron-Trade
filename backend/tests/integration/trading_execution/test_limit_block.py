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
        json={"api_key": "bnc_limit12345", "secret_key": "sec_limit12345"},
        headers=headers,
    )


def test_weekly_limit_exceeded_is_blocked(test_client):
    headers, user_id = _auth_headers(test_client, "exec-limit@example.com")
    subscription_store.set_status(user_id, "free", "active")
    _save_credentials(test_client, headers)

    first = {
        "requestId": "req-limit-1",
        "source": "MANUAL",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 50,
        "isSimulation": False,
    }
    second = dict(first)
    second["requestId"] = "req-limit-2"

    assert test_client.post("/v1/trading/executions", json=first, headers=headers).status_code == 201
    blocked = test_client.post("/v1/trading/executions", json=second, headers=headers)
    assert blocked.status_code == 201
    assert blocked.json()["status"] == "BLOCKED"
    assert blocked.json()["blockedReason"] == "weekly_limit_exceeded"
