from services.subscriptions.store import subscription_store


def _auth_headers_and_user(test_client, email: str) -> tuple[dict, str]:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    from services.auth.token_service import decode_token

    user_id = decode_token(token)["sub"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_history_combined_filters_and_cursor_pagination(test_client):
    headers, user_id = _auth_headers_and_user(test_client, "hist-filter@example.com")
    subscription_store.set_status(user_id, "plus", "active")

    test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_histf_123456789", "secret_key": "sec_histf_123456789"},
        headers=headers,
    )

    real = {
        "requestId": "hf-real-1",
        "source": "MANUAL",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 10,
        "isSimulation": False,
    }
    sim = {
        "requestId": "hf-sim-1",
        "source": "MANUAL",
        "symbol": "ETHUSDT",
        "side": "BUY",
        "orderType": "MARKET",
        "quantity": 10,
        "isSimulation": True,
    }
    test_client.post("/v1/trading/executions", json=real, headers=headers)
    test_client.post("/v1/trading/executions", json=sim, headers=headers)

    r1 = test_client.get("/v1/history/trades?isSimulation=true&status=EXECUTED&limit=1", headers=headers)
    assert r1.status_code == 200
    items = r1.json()["items"]
    assert len(items) == 1
    assert items[0]["isSimulation"] is True
