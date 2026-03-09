def test_users_me_with_refresh_token_is_rejected(test_client):
    credentials = {"email": "wrongtype@example.com", "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)

    refresh_token = login.json()["refreshToken"]
    response = test_client.get("/v1/users/me", headers={"Authorization": f"Bearer {refresh_token}"})

    assert response.status_code == 401
