def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


def test_invalid_token_is_dropped_and_deactivated(test_client):
    headers = _auth_headers(test_client, "notif-invalid@example.com")
    test_client.post(
        "/v1/notifications/device-tokens",
        json={"deviceId": "device-i-1", "platform": "ANDROID", "pushToken": "invalid_token_1234567890"},
        headers=headers,
    )

    emit = test_client.post(
        "/v1/notifications/emit",
        json={
            "eventId": "evt-invalid-1",
            "category": "SECURITY",
            "priority": "HIGH",
            "title": "Security alert",
            "message": "invalid token test",
        },
        headers=headers,
    )
    assert emit.status_code == 200
    assert emit.json()["items"][0]["status"] == "DROPPED"

    listed = test_client.get("/v1/notifications/device-tokens", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["items"] == []
