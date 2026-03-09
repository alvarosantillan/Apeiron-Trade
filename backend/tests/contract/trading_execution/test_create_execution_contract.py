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
    response = test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_exec12345", "secret_key": "sec_exec12345"},
        headers=headers,
    )
    assert response.status_code == 200


def test_create_execution_returns_201_and_shape(test_client):
    headers, user_id = _auth_headers(test_client, "exec-contract@example.com")
    subscription_store.set_status(user_id, "plus", "active")
    _save_credentials(test_client, headers)

    payload = {
        "requestId": "reqexec01",
        "source": "MANUAL",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 50,
        "isSimulation": False,
    }

    response = test_client.post("/v1/trading/executions", json=payload, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["requestId"] == payload["requestId"]
    assert body["executionType"] == "REAL"
    assert body["status"] == "EXECUTED"
    assert "id" in body


def test_create_execution_replays_same_request_id(test_client):
    headers, user_id = _auth_headers(test_client, "exec-replay@example.com")
    subscription_store.set_status(user_id, "plus", "active")
    _save_credentials(test_client, headers)

    payload = {
        "requestId": "reqreplay1",
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
    assert second.json()["id"] == first.json()["id"]
