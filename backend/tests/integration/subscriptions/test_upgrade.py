def test_transition_upgrade_to_premium(test_client):
    initial = test_client.get("/v1/subscriptions/status", headers={"x-user-id": "user-upgrade"})
    assert initial.status_code == 200
    assert initial.json()["planCode"] == "free"

    transition = test_client.post(
        "/v1/subscriptions/transition",
        json={"targetPlanCode": "premium"},
        headers={"x-user-id": "user-upgrade"},
    )
    assert transition.status_code == 200
    body = transition.json()
    assert body["planCode"] == "premium"
    assert body["status"] == "active"
    assert body["cancelAtPeriodEnd"] is False
