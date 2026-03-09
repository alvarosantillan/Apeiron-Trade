def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


def test_notification_history_persists_after_emit(test_client):
    headers = _auth_headers(test_client, "notif-history@example.com")

    token_payload = {
        "deviceId": "persist-device-1",
        "platform": "ANDROID",
        "pushToken": "token_valid_history_12345",
    }
    test_client.post("/v1/notifications/device-tokens", json=token_payload, headers=headers)

    emit_payload = {
        "eventId": "event-persist-001",
        "category": "TRADING",
        "priority": "HIGH",
        "title": "Trade updated",
        "message": "Execution completed",
    }
    emitted = test_client.post("/v1/notifications/emit", json=emit_payload, headers=headers)
    assert emitted.status_code == 200

    restarted = test_client.__class__(test_client.app)
    history = restarted.get("/v1/notifications/history", headers=headers)

    assert history.status_code == 200
    items = history.json()["items"]
    assert any(item["eventId"] == "event-persist-001" for item in items)
