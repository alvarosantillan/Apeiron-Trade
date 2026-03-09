from services.subscriptions.store import subscription_store


def _register_and_auth(test_client, email: str) -> tuple[dict, str]:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    access = login.json()["accessToken"]

    from services.auth.token_service import decode_token

    user_id = decode_token(access)["sub"]
    return {"Authorization": f"Bearer {access}"}, user_id


def test_restart_survives_auth_execution_notifications_and_ai_config(test_client):
    headers, user_id = _register_and_auth(test_client, "persist-all@example.com")

    subscription_store.set_status(user_id, "plus", "active")

    test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_exec12345", "secret_key": "sec_exec12345"},
        headers=headers,
    )

    test_client.post(
        "/v1/trading/executions",
        json={
            "requestId": "reqpersist1",
            "source": "MANUAL",
            "symbol": "BTCUSDT",
            "side": "BUY",
            "orderType": "MARKET",
            "quantity": 1,
            "isSimulation": False,
        },
        headers=headers,
    )

    test_client.post(
        "/v1/notifications/device-tokens",
        json={"deviceId": "dev1", "platform": "ANDROID", "pushToken": "token_valid_persist_123"},
        headers=headers,
    )
    test_client.post(
        "/v1/notifications/emit",
        json={
            "eventId": "persist-evt-1",
            "category": "TRADING",
            "priority": "HIGH",
            "title": "T",
            "message": "M",
        },
        headers=headers,
    )

    test_client.put(
        "/v1/ai-agent/config",
        json={
            "provider": "OPENAI",
            "apiKey": "ai_valid_key_123",
            "strategyId": "11111111-1111-1111-1111-111111111111",
            "riskProfile": "MEDIUM",
            "mode": "MANUAL",
            "isActive": True,
        },
        headers=headers,
    )

    restarted = test_client.__class__(test_client.app)

    history = restarted.get("/v1/trading/executions", headers=headers)
    notif = restarted.get("/v1/notifications/history", headers=headers)
    config = restarted.get("/v1/ai-agent/config", headers=headers)

    assert history.status_code == 200
    assert len(history.json()["items"]) >= 1
    assert notif.status_code == 200
    assert any(item["eventId"] == "persist-evt-1" for item in notif.json()["items"])
    assert config.status_code == 200
    assert config.json()["provider"] == "OPENAI"
