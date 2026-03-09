def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


def test_marketing_disabled_but_critical_override_allows_delivery(test_client):
    headers = _auth_headers(test_client, "notif-pref-filter@example.com")

    test_client.post(
        "/v1/notifications/device-tokens",
        json={"deviceId": "device-pf-1", "platform": "IOS", "pushToken": "token_ok_9876543210000"},
        headers=headers,
    )
    test_client.put(
        "/v1/notifications/preferences",
        json={"items": [{"category": "MARKETING", "enabled": False}, {"category": "TRADING", "enabled": True}]},
        headers=headers,
    )

    marketing_normal = test_client.post(
        "/v1/notifications/emit",
        json={
            "eventId": "evt-mkt-1",
            "category": "MARKETING",
            "priority": "LOW",
            "title": "Promo",
            "message": "discount",
        },
        headers=headers,
    )
    assert marketing_normal.status_code == 200
    assert marketing_normal.json()["items"] == []

    marketing_critical = test_client.post(
        "/v1/notifications/emit",
        json={
            "eventId": "evt-mkt-2",
            "category": "MARKETING",
            "priority": "CRITICAL",
            "title": "Urgent",
            "message": "critical notice",
        },
        headers=headers,
    )
    assert marketing_critical.status_code == 200
    assert len(marketing_critical.json()["items"]) == 1
