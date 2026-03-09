from __future__ import annotations

import os
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from services.persistence.models.base import Base


def _default_db_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./trdia.db")


def _engine_options(url: str) -> dict:
    if url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {"pool_pre_ping": True}


_engine: Engine | None = None
_session_local: sessionmaker[Session] | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        url = _default_db_url()
        _engine = create_engine(url, future=True, **_engine_options(url))
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    global _session_local
    if _session_local is None:
        _session_local = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)
    return _session_local


def reset_database_engine() -> None:
    global _engine, _session_local
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _session_local = None


def initialize_database() -> None:
    Base.metadata.create_all(bind=get_engine())


@contextmanager
def session_scope() -> Session:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
