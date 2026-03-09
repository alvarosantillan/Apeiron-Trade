from services.subscriptions.store import subscription_store


def _auth_headers_and_user(test_client, email: str) -> tuple[dict, str]:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    from services.auth.token_service import decode_token

    user_id = decode_token(token)["sub"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_history_contract_returns_items_and_next_cursor(test_client):
    headers, user_id = _auth_headers_and_user(test_client, "history-contract@example.com")
    subscription_store.set_status(user_id, "plus", "active")

    test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_histcontract_123", "secret_key": "sec_histcontract_123"},
        headers=headers,
    )

    for idx in range(2):
        test_client.post(
            "/v1/trading/executions",
            json={
                "requestId": f"hist-req-{idx}",
                "source": "MANUAL",
                "symbol": "BTCUSDT",
                "side": "BUY",
                "orderType": "MARKET",
                "quantity": 10,
                "isSimulation": False,
            },
            headers=headers,
        )

    response = test_client.get("/v1/history/trades?limit=1", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    assert "nextCursor" in body
