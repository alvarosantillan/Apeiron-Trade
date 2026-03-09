from services.subscriptions.store import subscription_store


def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def test_decision_fallback_on_provider_failure(test_client):
    headers = _auth_headers(test_client, "ai-fallback@example.com")

    from services.auth.token_service import decode_token

    user_id = decode_token(headers["Authorization"].removeprefix("Bearer "))["sub"]
    subscription_store.set_status(user_id, "plus", "active")

    config_payload = {
        "provider": "GEMINI",
        "apiKey": "ai_valid_provider_fail",
        "strategyId": "11111111-1111-1111-1111-111111111111",
        "riskProfile": "HIGH",
        "mode": "MANUAL",
        "isActive": True,
    }
    save = test_client.put("/v1/ai-agent/config", json=config_payload, headers=headers)
    assert save.status_code == 200

    run = test_client.post(
        "/v1/ai-agent/decisions/generate",
        json={"symbol": "FAILUSDT", "timeframe": "15m"},
        headers=headers,
    )
    assert run.status_code == 200
    body = run.json()
    assert body["action"] == "HOLD"
    assert body["status"] == "FALLBACK_HOLD"
    assert body["fallbackReason"] is not None
