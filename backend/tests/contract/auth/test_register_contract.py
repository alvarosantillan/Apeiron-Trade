def test_register_returns_201_and_user_shape(test_client):
    response = test_client.post(
        "/v1/auth/register",
        json={"email": "user1@example.com", "password": "Password123"},
    )

    assert response.status_code == 201
    body = response.json()
    assert "userId" in body
    assert body["email"] == "user1@example.com"


def test_register_duplicate_returns_409(test_client):
    payload = {"email": "dup@example.com", "password": "Password123"}
    test_client.post("/v1/auth/register", json=payload)
    second = test_client.post("/v1/auth/register", json=payload)

    assert second.status_code == 409
