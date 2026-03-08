from services.auth.token_service import create_access_token, create_refresh_token
from services.auth.user_store import store


class OAuthTokenError(ValueError):
    pass


def _parse_token(raw_token: str, expected_prefix: str) -> tuple[str, str]:
    parts = raw_token.split(":")
    if len(parts) != 3:
        raise OAuthTokenError("invalid_oauth_token")
    prefix, email, oauth_id = parts
    if prefix != expected_prefix or "@" not in email or not oauth_id:
        raise OAuthTokenError("invalid_oauth_token")
    return email, oauth_id


def login_with_google(id_token: str) -> dict[str, str]:
    email, oauth_id = _parse_token(id_token, "valid-google")
    user = store.find_or_create_oauth_user("google", oauth_id, email)
    access_token = create_access_token(user["id"], user["email"])
    refresh_token = create_refresh_token(user["id"])
    store.save_refresh_token(user["id"], refresh_token)
    return {"accessToken": access_token, "refreshToken": refresh_token}


def login_with_facebook(access_token: str) -> dict[str, str]:
    email, oauth_id = _parse_token(access_token, "valid-facebook")
    user = store.find_or_create_oauth_user("facebook", oauth_id, email)
    access_token_jwt = create_access_token(user["id"], user["email"])
    refresh_token = create_refresh_token(user["id"])
    store.save_refresh_token(user["id"], refresh_token)
    return {"accessToken": access_token_jwt, "refreshToken": refresh_token}
