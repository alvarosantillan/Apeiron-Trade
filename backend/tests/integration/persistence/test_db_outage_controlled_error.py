from services.persistence.errors import PersistenceUnavailableError


def test_db_outage_returns_controlled_error(test_client, monkeypatch):
    from services.auth import user_store

    def fail_create_user(*args, **kwargs):
        raise PersistenceUnavailableError("Persistence backend is unavailable")

    monkeypatch.setattr(user_store.store, "create_user", fail_create_user)

    response = test_client.post(
        "/v1/auth/register",
        json={"email": "db-outage@example.com", "password": "Password123"},
    )

    assert response.status_code == 503
    body = response.json()
    assert body["code"] == "DB_UNAVAILABLE"
    assert "traceId" in body
