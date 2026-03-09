from services.subscriptions.store import subscription_store


def _auth_headers_and_user(test_client, email: str) -> tuple[dict, str]:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    from services.auth.token_service import decode_token

    user_id = decode_token(token)["sub"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_trade_detail_contract(test_client):
    headers, user_id = _auth_headers_and_user(test_client, "trade-detail-contract@example.com")
    subscription_store.set_status(user_id, "plus", "active")
    test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_tdetail_123456", "secret_key": "sec_tdetail_123456"},
        headers=headers,
    )

    created = test_client.post(
        "/v1/trading/executions",
        json={
            "requestId": "detail-req-1",
            "source": "MANUAL",
            "symbol": "BTCUSDT",
            "side": "BUY",
            "orderType": "MARKET",
            "quantity": 10,
            "isSimulation": False,
        },
        headers=headers,
    )
    trade_id = created.json()["id"]

    response = test_client.get(f"/v1/history/trades/{trade_id}", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["tradeId"] == trade_id
    assert body["requestId"] == "detail-req-1"
