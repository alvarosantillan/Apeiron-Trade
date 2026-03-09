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
        json={"api_key": "bnc_paper12345", "secret_key": "sec_paper12345"},
        headers=headers,
    )


def test_paper_execution_does_not_increment_real_counter(test_client):
    headers, user_id = _auth_headers(test_client, "exec-paper@example.com")
    subscription_store.set_status(user_id, "free", "active")
    _save_credentials(test_client, headers)

    real_payload = {
        "requestId": "req-paper-real-1",
        "source": "MANUAL",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 50,
        "isSimulation": False,
    }
    assert test_client.post("/v1/trading/executions", json=real_payload, headers=headers).json()["status"] == "EXECUTED"

    paper_payload = {
        "requestId": "req-paper-sim-1",
        "source": "MANUAL",
        "symbol": "ETHUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 400,
        "isSimulation": True,
    }
    sim = test_client.post("/v1/trading/executions", json=paper_payload, headers=headers)
    assert sim.status_code == 201
    assert sim.json()["executionType"] == "PAPER"

    blocked_payload = dict(real_payload)
    blocked_payload["requestId"] = "req-paper-real-2"
    blocked = test_client.post("/v1/trading/executions", json=blocked_payload, headers=headers)
    assert blocked.status_code == 201
    assert blocked.json()["status"] == "BLOCKED"
    assert blocked.json()["blockedReason"] == "weekly_limit_exceeded"
