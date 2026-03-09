import os

from services.validation.db_settings import load_db_settings


def test_host_container_override_uses_host_docker_internal(monkeypatch):
    monkeypatch.setenv("DB_HOST", "host.docker.internal")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "trdia")
    monkeypatch.setenv("DB_USER", "trdia")
    monkeypatch.setenv("DB_PASSWORD", "trdia")
    monkeypatch.delenv("DATABASE_URL", raising=False)

    settings = load_db_settings()

    assert settings.host == "host.docker.internal"
    assert "host.docker.internal" in settings.database_url
    assert settings.port == 5432

    os.environ.pop("DB_HOST", None)
