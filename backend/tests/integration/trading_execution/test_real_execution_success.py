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
    assert (
        test_client.post(
            "/v1/trading/binance/credentials",
            json={"api_key": "bnc_real12345", "secret_key": "sec_real12345"},
            headers=headers,
        ).status_code
        == 200
    )


def test_real_execution_success_and_fetch_by_id(test_client):
    headers, user_id = _auth_headers(test_client, "exec-success@example.com")
    subscription_store.set_status(user_id, "plus", "active")
    _save_credentials(test_client, headers)

    create_payload = {
        "requestId": "req-real-201",
        "source": "MANUAL",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 100,
        "isSimulation": False,
    }
    created = test_client.post("/v1/trading/executions", json=create_payload, headers=headers)
    assert created.status_code == 201
    body = created.json()

    fetched = test_client.get(f"/v1/trading/executions/{body['id']}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["status"] == "EXECUTED"
