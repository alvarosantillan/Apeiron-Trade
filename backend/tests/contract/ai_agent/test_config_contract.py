from services.subscriptions.store import subscription_store


def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def test_config_upsert_and_get(test_client):
    headers = _auth_headers(test_client, "ai-contract@example.com")

    payload = {
        "provider": "OPENAI",
        "apiKey": "ai_valid_key_123",
        "strategyId": "11111111-1111-1111-1111-111111111111",
        "riskProfile": "MEDIUM",
        "mode": "MANUAL",
        "isActive": True,
    }

    save = test_client.put("/v1/ai-agent/config", json=payload, headers=headers)
    assert save.status_code == 200
    body = save.json()
    assert body["provider"] == "OPENAI"
    assert "apiKey" not in body

    read = test_client.get("/v1/ai-agent/config", headers=headers)
    assert read.status_code == 200
    assert read.json()["strategyId"] == payload["strategyId"]

    restarted = test_client.__class__(test_client.app)
    persisted = restarted.get("/v1/ai-agent/config", headers=headers)
    assert persisted.status_code == 200
    assert persisted.json()["strategyId"] == payload["strategyId"]


def test_free_user_automatic_mode_blocked(test_client):
    headers = _auth_headers(test_client, "ai-free-block@example.com")

    from services.auth.token_service import decode_token

    user_id = decode_token(headers["Authorization"].removeprefix("Bearer "))["sub"]
    subscription_store.set_status(user_id, "free", "active")

    payload = {
        "provider": "GROQ",
        "apiKey": "ai_valid_key_456",
        "strategyId": "11111111-1111-1111-1111-111111111111",
        "riskProfile": "LOW",
        "mode": "AUTOMATIC",
        "isActive": True,
    }

    response = test_client.put("/v1/ai-agent/config", json=payload, headers=headers)
    assert response.status_code == 403
