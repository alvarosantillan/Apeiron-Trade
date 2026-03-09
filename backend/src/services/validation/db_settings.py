from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DBSettings:
    database_url: str
    host: str
    port: int
    name: str
    user: str


def load_db_settings() -> DBSettings:
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    name = os.getenv("DB_NAME", "trdia")
    user = os.getenv("DB_USER", "trdia")
    url = os.getenv("DATABASE_URL", f"postgresql+psycopg://{user}:{os.getenv('DB_PASSWORD', 'trdia')}@{host}:{port}/{name}")
    return DBSettings(database_url=url, host=host, port=port, name=name, user=user)
