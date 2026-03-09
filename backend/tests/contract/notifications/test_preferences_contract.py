def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


def test_update_preferences_contract(test_client):
    headers = _auth_headers(test_client, "notif-pref@example.com")
    payload = {
        "items": [
            {"category": "MARKETING", "enabled": False},
            {"category": "TRADING", "enabled": True},
        ]
    }

    updated = test_client.put("/v1/notifications/preferences", json=payload, headers=headers)
    assert updated.status_code == 200

    get_resp = test_client.get("/v1/notifications/preferences", headers=headers)
    assert get_resp.status_code == 200
    items = {x["category"]: x["enabled"] for x in get_resp.json()["items"]}
    assert items["MARKETING"] is False
    assert items["TRADING"] is True
