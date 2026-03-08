def test_google_oauth_returns_token_pair(test_client):
    response = test_client.post(
        "/v1/auth/oauth/google",
        json={"idToken": "valid-google:user.oauth@example.com:google-123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body.get("accessToken"), str)
    assert isinstance(body.get("refreshToken"), str)


def test_google_oauth_invalid_token_returns_401(test_client):
    response = test_client.post(
        "/v1/auth/oauth/google",
        json={"idToken": "bad-token"},
    )

    assert response.status_code == 401


def test_facebook_oauth_returns_token_pair(test_client):
    response = test_client.post(
        "/v1/auth/oauth/facebook",
        json={"accessToken": "valid-facebook:user.fb@example.com:fb-555"},
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body.get("accessToken"), str)
    assert isinstance(body.get("refreshToken"), str)
