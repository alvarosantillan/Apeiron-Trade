from services.auth.user_store import store


def create_session(user_id: str, refresh_token: str) -> None:
    store.save_refresh_token(user_id, refresh_token)


def is_valid_session(user_id: str, refresh_token: str) -> bool:
    return store.validate_refresh_token(user_id, refresh_token)


def revoke_session(user_id: str, refresh_token: str) -> None:
    store.revoke_refresh_token(user_id, refresh_token)


def revoke_all_sessions(user_id: str) -> None:
    store.revoke_all_refresh_tokens(user_id)
