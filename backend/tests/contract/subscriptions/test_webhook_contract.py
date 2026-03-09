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


def test_webhook_invalid_external_reference_returns_400(test_client):
    payload = {
        "eventId": "evt-3",
        "externalReference": "bad-reference",
        "eventType": "payment",
        "status": "approved",
    }

    hook = test_client.post(
        "/v1/subscriptions/webhook",
        json=payload,
        headers={"x-signature": "valid-signature"},
    )
    assert hook.status_code == 400


def test_webhook_rejected_updates_to_past_due(test_client):
    payload = {
        "eventId": "evt-4",
        "externalReference": "user-a:plus:chk-4",
        "eventType": "payment",
        "status": "rejected",
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
    assert body["status"] == "past_due"
