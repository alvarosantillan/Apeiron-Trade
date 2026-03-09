import os
from pathlib import Path

import pytest


@pytest.fixture
def sqlite_db_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    db_file = tmp_path / "trdia-test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file.as_posix()}")
    return db_file
