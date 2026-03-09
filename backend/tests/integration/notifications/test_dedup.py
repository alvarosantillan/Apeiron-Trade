def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


def test_same_event_id_is_deduplicated_per_device(test_client):
    headers = _auth_headers(test_client, "notif-dedup@example.com")
    test_client.post(
        "/v1/notifications/device-tokens",
        json={"deviceId": "device-d-1", "platform": "ANDROID", "pushToken": "token_dedup_1234567890"},
        headers=headers,
    )

    payload = {
        "eventId": "evt-dedup-1",
        "category": "TRADING",
        "priority": "HIGH",
        "title": "Dedup event",
        "message": "do not duplicate",
    }

    first = test_client.post("/v1/notifications/emit", json=payload, headers=headers)
    second = test_client.post("/v1/notifications/emit", json=payload, headers=headers)
    assert first.status_code == 200
    assert len(first.json()["items"]) == 1
    assert second.status_code == 200
    assert second.json()["items"] == []
