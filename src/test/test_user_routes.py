def create_user(client, username="logan"):
    response = client.post(
        "/api/v1/user/",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 201, response.json()
    return response.json()


def login_user(client, email="logan@example.com", password="secret123"):
    response = client.post(
        "/api/v1/user/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_create_user(client):
    data = create_user(client, "logan")

    assert "id" in data
    assert data["username"] == "logan"
    assert data["email"] == "logan@example.com"


def test_get_users(client):
    create_user(client, "user1")
    create_user(client, "user2")

    response = client.get("/api/v1/user/")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_user_by_id(client):
    user = create_user(client, "unique_user")

    response = client.get(f"/api/v1/user/{user['id']}")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["id"] == user["id"]
    assert data["username"] == "unique_user"


def test_get_user_not_found(client):
    response = client.get("/api/v1/user/999999")
    assert response.status_code == 404


def test_login_user(client):
    create_user(client, "logan")

    token_data = login_user(client)

    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_get_me(client):
    create_user(client, "logan")
    token_data = login_user(client)

    response = client.get(
        "/api/v1/user/me",
        headers=auth_headers(token_data["access_token"]),
    )
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["username"] == "logan"
    assert data["email"] == "logan@example.com"
