from services.subscriptions.store import subscription_store
from workers.execution_reconciliation_worker import reconcile_execution


def _auth_headers(test_client, email: str) -> tuple[dict, str]:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    from services.auth.token_service import decode_token

    user_id = decode_token(access_token)["sub"]
    return {"Authorization": f"Bearer {access_token}"}, user_id


def _save_credentials(test_client, headers: dict) -> None:
    test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_recon12345", "secret_key": "sec_recon12345"},
        headers=headers,
    )


def test_timeout_goes_to_reconciliation_and_resolves(test_client):
    headers, user_id = _auth_headers(test_client, "exec-recon@example.com")
    subscription_store.set_status(user_id, "plus", "active")
    _save_credentials(test_client, headers)

    payload = {
        "requestId": "req-recon-1",
        "source": "MANUAL",
        "symbol": "TIMEOUTUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 80,
        "isSimulation": False,
    }
    created = test_client.post("/v1/trading/executions", json=payload, headers=headers)
    assert created.status_code == 201
    execution_id = created.json()["id"]
    assert created.json()["status"] == "PENDING_RECONCILIATION"

    reconciled = reconcile_execution(execution_id)
    assert reconciled is not None
    assert reconciled["status"] in {"EXECUTED", "FAILED"}
