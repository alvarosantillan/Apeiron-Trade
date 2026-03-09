def test_login_returns_token_pair(test_client):
    register_payload = {"email": "login@example.com", "password": "Password123"}
    test_client.post("/v1/auth/register", json=register_payload)

    response = test_client.post("/v1/auth/login", json=register_payload)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body.get("accessToken"), str)
    assert isinstance(body.get("refreshToken"), str)
    assert body.get("tokenType") == "bearer"


def test_login_invalid_credentials_returns_401(test_client):
    response = test_client.post(
        "/v1/auth/login",
        json={"email": "missing@example.com", "password": "Password123"},
    )

    assert response.status_code == 401
