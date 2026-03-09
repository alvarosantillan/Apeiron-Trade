from services.auth.token_service import create_access_token, create_refresh_token, decode_token


def test_access_token_contains_expected_claims():
    token = create_access_token("user-1", "user@example.com")
    decoded = decode_token(token)

    assert decoded["sub"] == "user-1"
    assert decoded["type"] == "access"
    assert decoded["email"] == "user@example.com"
    assert decoded["exp"] > decoded["iat"]


def test_refresh_token_contains_jti_and_type():
    token = create_refresh_token("user-2")
    decoded = decode_token(token)

    assert decoded["sub"] == "user-2"
    assert decoded["type"] == "refresh"
    assert isinstance(decoded.get("jti"), str)
    assert decoded["exp"] > decoded["iat"]
