def test_refresh_session_survives_client_restart(test_client):
    creds = {"email": "session-persist@example.com", "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)

    refresh_token = login.json()["refreshToken"]
    restarted = test_client.__class__(test_client.app)

    refreshed = restarted.post("/v1/auth/refresh", json={"refreshToken": refresh_token})

    assert refreshed.status_code == 200
    assert isinstance(refreshed.json()["refreshToken"], str)
