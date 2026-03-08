from uuid import uuid4

from services.auth.password_service import hash_password, verify_password


class InMemoryUserStore:
    def __init__(self) -> None:
        self._users_by_email: dict[str, dict] = {}
        self._users_by_oauth: dict[str, dict] = {}
        self._refresh_tokens: dict[str, set[str]] = {}

    def create_user(self, email: str, password: str) -> dict:
        if email in self._users_by_email:
            raise ValueError("user_exists")
        user = {"id": str(uuid4()), "email": email, "password_hash": hash_password(password)}
        self._users_by_email[email] = user
        return user

    def authenticate(self, email: str, password: str) -> dict | None:
        user = self._users_by_email.get(email)
        if not user:
            return None
        if not user["password_hash"]:
            return None
        if not verify_password(password, user["password_hash"]):
            return None
        return user

    def save_refresh_token(self, user_id: str, refresh_token: str) -> None:
        if user_id not in self._refresh_tokens:
            self._refresh_tokens[user_id] = set()
        self._refresh_tokens[user_id].add(refresh_token)

    def validate_refresh_token(self, user_id: str, refresh_token: str) -> bool:
        return refresh_token in self._refresh_tokens.get(user_id, set())

    def revoke_refresh_token(self, user_id: str, refresh_token: str) -> None:
        tokens = self._refresh_tokens.get(user_id)
        if not tokens:
            return
        tokens.discard(refresh_token)

    def revoke_all_refresh_tokens(self, user_id: str) -> None:
        self._refresh_tokens[user_id] = set()

    def find_or_create_oauth_user(self, provider: str, oauth_id: str, email: str) -> dict:
        key = f"{provider}:{oauth_id}"
        existing = self._users_by_oauth.get(key)
        if existing:
            return existing

        user = self._users_by_email.get(email)
        if not user:
            user = {"id": str(uuid4()), "email": email, "password_hash": None}
            self._users_by_email[email] = user

        self._users_by_oauth[key] = user
        return user


store = InMemoryUserStore()
