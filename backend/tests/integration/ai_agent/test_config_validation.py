def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def test_invalid_provider_credentials_rejected(test_client):
    headers = _auth_headers(test_client, "ai-invalid-key@example.com")
    payload = {
        "provider": "OPENAI",
        "apiKey": "invalid_key",
        "strategyId": "11111111-1111-1111-1111-111111111111",
        "riskProfile": "MEDIUM",
        "mode": "MANUAL",
        "isActive": True,
    }

    response = test_client.put("/v1/ai-agent/config", json=payload, headers=headers)
    assert response.status_code == 400
