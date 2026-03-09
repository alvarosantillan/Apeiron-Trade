from services.subscriptions.store import subscription_store


def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def test_free_plan_rejects_automatic_mode(test_client):
    headers = _auth_headers(test_client, "ai-free-restrict@example.com")

    from services.auth.token_service import decode_token

    user_id = decode_token(headers["Authorization"].removeprefix("Bearer "))["sub"]
    subscription_store.set_status(user_id, "free", "active")

    payload = {
        "provider": "DEEPSEEK",
        "apiKey": "ai_valid_auto_123",
        "strategyId": "11111111-1111-1111-1111-111111111111",
        "riskProfile": "LOW",
        "mode": "AUTOMATIC",
        "isActive": True,
    }

    response = test_client.put("/v1/ai-agent/config", json=payload, headers=headers)
    assert response.status_code == 403
