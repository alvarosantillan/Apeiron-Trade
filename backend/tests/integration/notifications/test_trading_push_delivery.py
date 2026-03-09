def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


def test_trading_event_push_delivery(test_client):
    headers = _auth_headers(test_client, "notif-trading@example.com")
    test_client.post(
        "/v1/notifications/device-tokens",
        json={"deviceId": "device-tr-1", "platform": "ANDROID", "pushToken": "token_ok_1234567890123"},
        headers=headers,
    )

    emit = test_client.post(
        "/v1/notifications/emit",
        json={
            "eventId": "evt-trading-1",
            "category": "TRADING",
            "priority": "HIGH",
            "title": "Trade executed",
            "message": "BTCUSDT BUY executed",
            "referenceId": "trade-1",
        },
        headers=headers,
    )
    assert emit.status_code == 200
    assert emit.json()["items"][0]["status"] in {"SENT", "DELIVERED"}
