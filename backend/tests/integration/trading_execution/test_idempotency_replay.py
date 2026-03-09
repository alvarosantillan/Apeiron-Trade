from services.subscriptions.store import subscription_store


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
        json={"api_key": "bnc_idem12345", "secret_key": "sec_idem12345"},
        headers=headers,
    )


def test_same_request_id_replays_same_execution_without_duplicate(test_client):
    headers, user_id = _auth_headers(test_client, "exec-idem@example.com")
    subscription_store.set_status(user_id, "plus", "active")
    _save_credentials(test_client, headers)

    payload = {
        "requestId": "req-idem-1",
        "source": "MANUAL",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 25,
        "isSimulation": False,
    }

    first = test_client.post("/v1/trading/executions", json=payload, headers=headers)
    second = test_client.post("/v1/trading/executions", json=payload, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] == second.json()["id"]

    listed = test_client.get("/v1/trading/executions?limit=50", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()["items"]) == 1
