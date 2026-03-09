def test_duplicate_webhook_event_is_ignored(test_client):
    first = {
        "eventId": "evt-dedup-1",
        "externalReference": "user-dedup:plus:chk-1",
        "eventType": "payment",
        "status": "approved",
    }

    second_duplicate = {
        "eventId": "evt-dedup-1",
        "externalReference": "user-dedup:premium:chk-2",
        "eventType": "payment",
        "status": "approved",
    }

    hook_1 = test_client.post(
        "/v1/subscriptions/webhook",
        json=first,
        headers={"x-signature": "valid-signature"},
    )
    assert hook_1.status_code == 204

    status_after_first = test_client.get("/v1/subscriptions/status", headers={"x-user-id": "user-dedup"})
    assert status_after_first.status_code == 200
    assert status_after_first.json()["planCode"] == "plus"

    hook_2 = test_client.post(
        "/v1/subscriptions/webhook",
        json=second_duplicate,
        headers={"x-signature": "valid-signature"},
    )
    assert hook_2.status_code == 204

    status_after_second = test_client.get("/v1/subscriptions/status", headers={"x-user-id": "user-dedup"})
    assert status_after_second.status_code == 200
    assert status_after_second.json()["planCode"] == "plus"
