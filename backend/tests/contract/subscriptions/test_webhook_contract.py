def test_webhook_requires_signature(test_client):
    payload = {
        "eventId": "evt-1",
        "externalReference": "user-a:plus:chk-1",
        "eventType": "payment",
        "status": "approved",
    }
    response = test_client.post("/v1/subscriptions/webhook", json=payload)
    assert response.status_code == 401


def test_webhook_approved_updates_subscription_status(test_client):
    payload = {
        "eventId": "evt-2",
        "externalReference": "user-a:plus:chk-2",
        "eventType": "payment",
        "status": "approved",
    }

    hook = test_client.post(
        "/v1/subscriptions/webhook",
        json=payload,
        headers={"x-signature": "valid-signature"},
    )
    assert hook.status_code == 204

    status = test_client.get("/v1/subscriptions/status", headers={"x-user-id": "user-a"})
    assert status.status_code == 200
    body = status.json()
    assert body["planCode"] == "plus"
    assert body["status"] == "active"
