def test_checkout_then_webhook_activates_plan(test_client):
    checkout = test_client.post(
        "/v1/subscriptions/checkout",
        json={"planCode": "premium"},
        headers={"x-user-id": "user-plan-1"},
    )
    assert checkout.status_code == 200

    webhook_payload = {
        "eventId": "evt-100",
        "externalReference": "user-plan-1:premium:chk-100",
        "eventType": "payment",
        "status": "approved",
    }

    hook = test_client.post(
        "/v1/subscriptions/webhook",
        json=webhook_payload,
        headers={"x-signature": "valid-signature"},
    )
    assert hook.status_code == 204

    status = test_client.get("/v1/subscriptions/status", headers={"x-user-id": "user-plan-1"})
    assert status.status_code == 200
    body = status.json()
    assert body["planCode"] == "premium"
    assert body["status"] == "active"
