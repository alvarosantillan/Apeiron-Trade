from services.subscriptions.store import subscription_store


def _auth_headers_and_user(test_client, email: str) -> tuple[dict, str]:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    from services.auth.token_service import decode_token

    user_id = decode_token(token)["sub"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_dashboard_load_for_active_user(test_client):
    headers, user_id = _auth_headers_and_user(test_client, "dash-load@example.com")
    subscription_store.set_status(user_id, "plus", "active")

    response = test_client.get("/v1/dashboard/summary", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["planCode"] == "plus"
    assert body["operationsLimit"] == 10
