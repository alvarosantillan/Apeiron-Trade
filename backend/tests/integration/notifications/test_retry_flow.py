def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


def test_transient_failure_ends_in_failed_after_retries(test_client):
    headers = _auth_headers(test_client, "notif-retry@example.com")
    test_client.post(
        "/v1/notifications/device-tokens",
        json={"deviceId": "device-r-1", "platform": "ANDROID", "pushToken": "transient_token_1234567890"},
        headers=headers,
    )

    emit = test_client.post(
        "/v1/notifications/emit",
        json={
            "eventId": "evt-retry-1",
            "category": "TRADING",
            "priority": "HIGH",
            "title": "Trade retry",
            "message": "retry me",
        },
        headers=headers,
    )
    assert emit.status_code == 200
    assert emit.json()["items"][0]["status"] == "FAILED"
