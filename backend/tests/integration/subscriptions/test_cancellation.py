def test_cancel_at_period_end_marks_flag(test_client):
    test_client.post(
        "/v1/subscriptions/transition",
        json={"targetPlanCode": "plus"},
        headers={"x-user-id": "user-cancel"},
    )

    cancel = test_client.post(
        "/v1/subscriptions/cancel",
        json={"cancelAtPeriodEnd": True},
        headers={"x-user-id": "user-cancel"},
    )
    assert cancel.status_code == 200
    body = cancel.json()
    assert body["planCode"] == "plus"
    assert body["cancelAtPeriodEnd"] is True


def test_cancel_immediate_moves_user_to_free(test_client):
    test_client.post(
        "/v1/subscriptions/transition",
        json={"targetPlanCode": "premium"},
        headers={"x-user-id": "user-cancel-now"},
    )

    cancel = test_client.post(
        "/v1/subscriptions/cancel",
        json={"cancelAtPeriodEnd": False},
        headers={"x-user-id": "user-cancel-now"},
    )
    assert cancel.status_code == 200
    body = cancel.json()
    assert body["planCode"] == "free"
    assert body["status"] == "active"
    assert body["cancelAtPeriodEnd"] is False
