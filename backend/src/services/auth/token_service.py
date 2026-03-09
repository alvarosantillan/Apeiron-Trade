import os
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jose import jwt

ALGORITHM = "HS256"
ACCESS_TTL_MINUTES = 15
REFRESH_TTL_DAYS = 7
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-me")


def _encode(payload: dict, ttl: timedelta) -> str:
    now = datetime.now(timezone.utc)
    claims = {**payload, "iat": int(now.timestamp()), "exp": int((now + ttl).timestamp())}
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: str, email: str) -> str:
    return _encode({"sub": user_id, "email": email, "type": "access"}, timedelta(minutes=ACCESS_TTL_MINUTES))


def create_refresh_token(user_id: str) -> str:
    return _encode({"sub": user_id, "jti": str(uuid4()), "type": "refresh"}, timedelta(days=REFRESH_TTL_DAYS))


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
