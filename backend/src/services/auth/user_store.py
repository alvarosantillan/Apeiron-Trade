from uuid import uuid4

from services.auth.password_service import hash_password, verify_password
from services.persistence.database import session_scope
from services.persistence.models.base import AuthSessionModel, UserAccountModel, now_utc


class InMemoryUserStore:
    def __init__(self) -> None:
        self._users_by_oauth: dict[str, dict] = {}

    def create_user(self, email: str, password: str) -> dict:
        with session_scope() as session:
            existing = session.query(UserAccountModel).filter(UserAccountModel.email == email).first()
            if existing:
                raise ValueError("user_exists")
            user = UserAccountModel(id=str(uuid4()), email=email, password_hash=hash_password(password), created_at=now_utc())
            session.add(user)
            return {"id": user.id, "email": user.email, "password_hash": user.password_hash}

    def authenticate(self, email: str, password: str) -> dict | None:
        with session_scope() as session:
            user = session.query(UserAccountModel).filter(UserAccountModel.email == email).first()
            if not user:
                return None
            if not user.password_hash:
                return None
            if not verify_password(password, user.password_hash):
                return None
            return {"id": user.id, "email": user.email, "password_hash": user.password_hash}

    def save_refresh_token(self, user_id: str, refresh_token: str) -> None:
        with session_scope() as session:
            found = (
                session.query(AuthSessionModel)
                .filter(AuthSessionModel.user_id == user_id, AuthSessionModel.refresh_token == refresh_token)
                .first()
            )
            if found:
                found.revoked = False
                return
            session.add(
                AuthSessionModel(
                    id=str(uuid4()),
                    user_id=user_id,
                    refresh_token=refresh_token,
                    revoked=False,
                    created_at=now_utc(),
                )
            )

    def validate_refresh_token(self, user_id: str, refresh_token: str) -> bool:
        with session_scope() as session:
            found = (
                session.query(AuthSessionModel)
                .filter(AuthSessionModel.user_id == user_id, AuthSessionModel.refresh_token == refresh_token)
                .first()
            )
            return bool(found and not found.revoked)

    def revoke_refresh_token(self, user_id: str, refresh_token: str) -> None:
        with session_scope() as session:
            found = (
                session.query(AuthSessionModel)
                .filter(AuthSessionModel.user_id == user_id, AuthSessionModel.refresh_token == refresh_token)
                .first()
            )
            if found:
                found.revoked = True

    def revoke_all_refresh_tokens(self, user_id: str) -> None:
        with session_scope() as session:
            sessions = session.query(AuthSessionModel).filter(AuthSessionModel.user_id == user_id).all()
            for item in sessions:
                item.revoked = True

    def find_or_create_oauth_user(self, provider: str, oauth_id: str, email: str) -> dict:
        key = f"{provider}:{oauth_id}"
        existing = self._users_by_oauth.get(key)
        if existing:
            return existing

        with session_scope() as session:
            user = session.query(UserAccountModel).filter(UserAccountModel.email == email).first()
            if not user:
                user = UserAccountModel(id=str(uuid4()), email=email, password_hash=None, created_at=now_utc())
                session.add(user)
            payload = {"id": user.id, "email": user.email, "password_hash": user.password_hash}
            self._users_by_oauth[key] = payload
            return payload

    def get_user_by_id(self, user_id: str) -> dict | None:
        with session_scope() as session:
            user = session.query(UserAccountModel).filter(UserAccountModel.id == user_id).first()
            if not user:
                return None
            return {"id": user.id, "email": user.email, "password_hash": user.password_hash}

    def reset_for_tests(self) -> None:
        self._users_by_oauth.clear()


store = InMemoryUserStore()
