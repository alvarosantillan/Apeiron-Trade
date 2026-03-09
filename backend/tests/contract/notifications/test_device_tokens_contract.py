def _auth_headers(test_client, email: str) -> dict:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


def test_upsert_and_list_device_tokens(test_client):
    headers = _auth_headers(test_client, "notif-device@example.com")

    payload = {
        "deviceId": "device-1",
        "platform": "ANDROID",
        "pushToken": "token_valid_1234567890",
    }
    created = test_client.post("/v1/notifications/device-tokens", json=payload, headers=headers)
    assert created.status_code == 200
    body = created.json()
    assert body["deviceId"] == "device-1"
    assert "pushToken" not in body

    listed = test_client.get("/v1/notifications/device-tokens", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()["items"]) == 1
