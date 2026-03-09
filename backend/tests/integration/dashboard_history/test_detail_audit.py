from services.audit.trade_detail_audit import trade_detail_audit_store
from services.subscriptions.store import subscription_store


def _auth_headers_and_user(test_client, email: str) -> tuple[dict, str]:
    creds = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=creds)
    login = test_client.post("/v1/auth/login", json=creds)
    token = login.json()["accessToken"]
    from services.auth.token_service import decode_token

    user_id = decode_token(token)["sub"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_trade_detail_access_writes_audit_event(test_client):
    headers, user_id = _auth_headers_and_user(test_client, "detail-audit@example.com")
    subscription_store.set_status(user_id, "plus", "active")

    test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_daudit_1234567", "secret_key": "sec_daudit_1234567"},
        headers=headers,
    )
    created = test_client.post(
        "/v1/trading/executions",
        json={
            "requestId": "da-00001",
            "source": "MANUAL",
            "symbol": "BTCUSDT",
            "side": "BUY",
            "orderType": "MARKET",
            "quantity": 5,
            "isSimulation": False,
        },
        headers=headers,
    )

    trade_id = created.json()["id"]
    detail = test_client.get(f"/v1/history/trades/{trade_id}", headers=headers)
    assert detail.status_code == 200
    assert len(trade_detail_audit_store._events) == 1
    assert trade_detail_audit_store._events[0]["tradeId"] == trade_id
