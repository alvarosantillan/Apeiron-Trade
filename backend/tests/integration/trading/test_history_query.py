def _auth_headers(test_client, email: str) -> dict:
    credentials = {"email": email, "password": "Password123"}
    test_client.post("/v1/auth/register", json=credentials)
    login = test_client.post("/v1/auth/login", json=credentials)
    access_token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


def _save_credentials(test_client, headers: dict) -> None:
    response = test_client.post(
        "/v1/trading/binance/credentials",
        json={"api_key": "bnc_hist12345", "secret_key": "sec_hist12345"},
        headers=headers,
    )
    assert response.status_code == 200


def test_trade_history_filters_and_pagination(test_client):
    headers = _auth_headers(test_client, "trade-history@example.com")
    _save_credentials(test_client, headers)

    real_payload = {
        "request_id": "req-hist-real-1",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 100,
        "is_simulation": False,
        "source": "manual",
    }
    paper_payload = {
        "request_id": "req-hist-paper-1",
        "symbol": "ETHUSDT",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 200,
        "is_simulation": True,
        "source": "manual",
    }

    assert test_client.post("/v1/trading/execute", json=real_payload, headers=headers).status_code == 200
    assert test_client.post("/v1/trading/execute", json=paper_payload, headers=headers).status_code == 200

    only_paper = test_client.get("/v1/trading/history?is_simulation=true", headers=headers)
    assert only_paper.status_code == 200
    paper_body = only_paper.json()
    assert paper_body["total"] == 1
    assert paper_body["items"][0]["execution_type"] == "PAPER"

    paged = test_client.get("/v1/trading/history?page=1&page_size=1", headers=headers)
    assert paged.status_code == 200
    paged_body = paged.json()
    assert paged_body["page"] == 1
    assert paged_body["page_size"] == 1
    assert paged_body["total"] == 2
    assert len(paged_body["items"]) == 1
