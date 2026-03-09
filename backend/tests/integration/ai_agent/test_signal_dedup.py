from services.subscriptions.store import subscription_store


def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def test_equivalent_signal_is_deduplicated(test_client):
    headers = _auth_headers(test_client, "ai-dedup@example.com")

    from services.auth.token_service import decode_token

    user_id = decode_token(headers["Authorization"].removeprefix("Bearer "))["sub"]
    subscription_store.set_status(user_id, "plus", "active")

    config_payload = {
        "provider": "OPENAI",
        "apiKey": "ai_valid_dedup_123",
        "strategyId": "11111111-1111-1111-1111-111111111111",
        "riskProfile": "MEDIUM",
        "mode": "MANUAL",
        "isActive": True,
    }
    assert test_client.put("/v1/ai-agent/config", json=config_payload, headers=headers).status_code == 200

    payload = {"symbol": "BTCUSDT", "timeframe": "1h"}
    first = test_client.post("/v1/ai-agent/decisions/generate", json=payload, headers=headers)
    second = test_client.post("/v1/ai-agent/decisions/generate", json=payload, headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]

    listed = test_client.get("/v1/ai-agent/decisions?limit=10", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()["items"]) == 1
