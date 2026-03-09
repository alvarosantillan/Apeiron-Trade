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


def test_refresh_token_remains_valid_across_client_restart(test_client):
    creds = {"email": "refresh-persist@example.com", "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login_response = test_client.post("/v1/auth/login", json=creds)
    refresh_token = login_response.json()["refreshToken"]

    restarted = test_client.__class__(test_client.app)
    refresh_response = restarted.post("/v1/auth/refresh", json={"refreshToken": refresh_token})

    assert refresh_response.status_code == 200
    body = refresh_response.json()
    assert isinstance(body.get("accessToken"), str)
    assert isinstance(body.get("refreshToken"), str)
