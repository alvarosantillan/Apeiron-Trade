from uuid import uuid4

from services.auth.password_service import hash_password, verify_password


class InMemoryUserStore:
    def __init__(self) -> None:
        self._users_by_email: dict[str, dict] = {}
        self._refresh_tokens: dict[str, str] = {}

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
        if not verify_password(password, user["password_hash"]):
            return None
        return user

    def save_refresh_token(self, user_id: str, refresh_token: str) -> None:
        self._refresh_tokens[user_id] = refresh_token

    def validate_refresh_token(self, user_id: str, refresh_token: str) -> bool:
        return self._refresh_tokens.get(user_id) == refresh_token


store = InMemoryUserStore()
