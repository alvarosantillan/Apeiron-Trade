from services.subscriptions.store import subscription_store


def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def test_decision_generation_success(test_client):
    headers = _auth_headers(test_client, "ai-decision-success@example.com")

    from services.auth.token_service import decode_token

    user_id = decode_token(headers["Authorization"].removeprefix("Bearer "))["sub"]
    subscription_store.set_status(user_id, "plus", "active")

    config_payload = {
        "provider": "OPENAI",
        "apiKey": "ai_valid_success_123",
        "strategyId": "11111111-1111-1111-1111-111111111111",
        "riskProfile": "MEDIUM",
        "mode": "MANUAL",
        "isActive": True,
    }
    save = test_client.put("/v1/ai-agent/config", json=config_payload, headers=headers)
    assert save.status_code == 200

    run = test_client.post(
        "/v1/ai-agent/decisions/generate",
        json={"symbol": "BTCUSDT", "timeframe": "1h"},
        headers=headers,
    )
    assert run.status_code == 200
    body = run.json()
    assert body["action"] in {"BUY", "SELL", "HOLD"}
    assert body["status"] == "PENDING_APPROVAL"

    listed = test_client.get("/v1/ai-agent/decisions?limit=5", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["items"][0]["id"] == body["id"]
