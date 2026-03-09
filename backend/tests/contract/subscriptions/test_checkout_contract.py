def test_checkout_plus_returns_url(test_client):
    response = test_client.post(
        "/v1/subscriptions/checkout",
        json={"planCode": "plus"},
        headers={"x-user-id": "user-a"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "mercadopago"
    assert body["checkoutUrl"].startswith("https://")


def test_checkout_free_is_rejected(test_client):
    response = test_client.post(
        "/v1/subscriptions/checkout",
        json={"planCode": "free"},
        headers={"x-user-id": "user-a"},
    )

    assert response.status_code == 400
