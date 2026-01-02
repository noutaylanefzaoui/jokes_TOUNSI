def register_user(client, email="test@example.com", password="secret123"):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "display_name": "Test User",
            "password": password,
        },
    )


def login_user(client, email="test@example.com", password="secret123"):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )


def test_register_and_login_flow(client):
    # Register
    resp = register_user(client)
    assert resp.status_code == 201

    # Login
    resp = login_user(client)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data

    # Use token on /users/me
    token = data["access_token"]
    resp = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    user = resp.get_json()
    assert user["email"] == "test@example.com"
