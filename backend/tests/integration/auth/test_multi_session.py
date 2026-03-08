def test_multi_session_logout_and_logout_all(test_client):
    credentials = {"email": "multi@example.com", "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)

    first_login = test_client.post("/v1/auth/login", json=credentials)
    second_login = test_client.post("/v1/auth/login", json=credentials)

    assert first_login.status_code == 200
    assert second_login.status_code == 200

    refresh_token_1 = first_login.json()["refreshToken"]
    refresh_token_2 = second_login.json()["refreshToken"]
    assert refresh_token_1 != refresh_token_2

    logout_1 = test_client.post("/v1/auth/logout", json={"refreshToken": refresh_token_1})
    assert logout_1.status_code == 204

    revoked_refresh = test_client.post("/v1/auth/refresh", json={"refreshToken": refresh_token_1})
    assert revoked_refresh.status_code == 401

    still_valid_refresh = test_client.post("/v1/auth/refresh", json={"refreshToken": refresh_token_2})
    assert still_valid_refresh.status_code == 200

    current_refresh = still_valid_refresh.json()["refreshToken"]
    logout_all = test_client.post("/v1/auth/logout-all", json={"refreshToken": current_refresh})
    assert logout_all.status_code == 204

    after_logout_all = test_client.post("/v1/auth/refresh", json={"refreshToken": current_refresh})
    assert after_logout_all.status_code == 401
