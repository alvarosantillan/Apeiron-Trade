from jose import jwt

from services.auth.token_service import ALGORITHM, SECRET_KEY


def _extract_sub(access_token: str) -> str:
    decoded = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded["sub"]


def test_google_oauth_same_identity_returns_same_user(test_client):
    payload = {"idToken": "valid-google:repeat@example.com:google-repeat-1"}

    first = test_client.post("/v1/auth/oauth/google", json=payload)
    second = test_client.post("/v1/auth/oauth/google", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200

    first_sub = _extract_sub(first.json()["accessToken"])
    second_sub = _extract_sub(second.json()["accessToken"])
    assert first_sub == second_sub
