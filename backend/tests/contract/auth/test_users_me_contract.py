def test_users_me_requires_bearer_token(test_client):
    response = test_client.get("/v1/users/me")
    assert response.status_code == 401


def test_users_me_returns_profile_for_authenticated_user(test_client):
    credentials = {"email": "me@example.com", "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)

    access_token = login.json()["accessToken"]
    response = test_client.get("/v1/users/me", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == credentials["email"]
    assert isinstance(body["userId"], str)
