def create_user(client, username="logan"):
    response = client.post(
        "/api/v1/user/",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "Secret123!",
        },
    )
    assert response.status_code == 201, response.json()
    return response.json()


def login_user(client, email="logan@example.com", password="Secret123!"):
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


def test_create_duplicate_user(client):
    create_user(client, "user1")
    response = client.post(
        "/api/v1/user/",
        json={
            "username": "user2",
            "email": "user1@example.com",
            "password": "Secret123!",
        },
    )
    assert response.status_code == 409


def test_create_duplicate_username(client):
    create_user(client, "user1")
    response = client.post(
        "/api/v1/user/",
        json={
            "username": "user1",
            "email": "different@example.com",
            "password": "Secret123!",
        },
    )
    assert response.status_code == 409


def test_create_user_requires_uppercase_password(client):
    response = client.post(
        "/api/v1/user/",
        json={
            "username": "nouppercase",
            "email": "nouppercase@example.com",
            "password": "secret123!",
        },
    )
    assert response.status_code == 422, response.json()
    assert "uppercase letter" in response.json()["detail"][0]["msg"]


def test_create_user_requires_special_character_password(client):
    response = client.post(
        "/api/v1/user/",
        json={
            "username": "nospecial",
            "email": "nospecial@example.com",
            "password": "Secret123",
        },
    )
    assert response.status_code == 422, response.json()
    assert "special character" in response.json()["detail"][0]["msg"]


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


def test_login_sets_auth_cookie(client):
    create_user(client, "cookieuser")

    response = client.post(
        "/api/v1/user/login",
        data={"username": "cookieuser@example.com", "password": "Secret123!"},
    )

    assert response.status_code == 200, response.json()
    assert response.cookies.get("vodle_access_token") is not None


def test_login_wrong_password(client):
    create_user(client, "logan")
    response = client.post(
        "/api/v1/user/login",
        data={"username": "logan@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


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


def test_get_me_with_cookie_auth(client):
    create_user(client, "cookieauth")

    login_response = client.post(
        "/api/v1/user/login",
        data={"username": "cookieauth@example.com", "password": "Secret123!"},
    )
    assert login_response.status_code == 200, login_response.json()

    response = client.get("/api/v1/user/me")
    assert response.status_code == 200, response.json()
    assert response.json()["email"] == "cookieauth@example.com"


def test_update_user(client):
    user = create_user(client, "logan")
    token_data = login_user(client)

    response = client.put(
        f"/api/v1/user/{user['id']}",
        json={"password": "Newpassword!"},
        headers=auth_headers(token_data["access_token"]),
    )
    assert response.status_code == 200


def test_update_user_unauthorized(client):
    user1 = create_user(client, "user1")
    create_user(client, "user2")
    token2 = login_user(client, "user2@example.com")["access_token"]

    response = client.put(
        f"/api/v1/user/{user1['id']}",
        json={"password": "Newpassword!"},
        headers=auth_headers(token2),
    )
    assert response.status_code == 403


def test_delete_user(client):
    user = create_user(client, "logan")
    token_data = login_user(client)

    response = client.delete(
        f"/api/v1/user/{user['id']}",
        headers=auth_headers(token_data["access_token"]),
    )
    assert response.status_code == 204


def test_delete_user_unauthorized(client):
    user1 = create_user(client, "user1")
    create_user(client, "user2")
    token2 = login_user(client, "user2@example.com")["access_token"]

    response = client.delete(
        f"/api/v1/user/{user1['id']}",
        headers=auth_headers(token2),
    )
    assert response.status_code == 403


def test_logout_clears_auth_cookie(client):
    create_user(client, "logoutuser")
    login_response = client.post(
        "/api/v1/user/login",
        data={"username": "logoutuser@example.com", "password": "Secret123!"},
    )
    assert login_response.status_code == 200, login_response.json()

    response = client.post("/api/v1/user/logout")
    assert response.status_code == 204

    me_response = client.get("/api/v1/user/me")
    assert me_response.status_code == 401


def test_get_my_stats(client, admin_token):
    create_user(client, "statsuser")
    token = login_user(client, "statsuser@example.com")["access_token"]

    question1 = client.post(
        "/api/v1/question/",
        json={
            "title": "Question one",
            "description": "First",
            "question_text": "First question?",
            "publish_date": "2026-04-21",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    question2 = client.post(
        "/api/v1/question/",
        json={
            "title": "Question two",
            "description": "Second",
            "question_text": "Second question?",
            "publish_date": "2026-04-22",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()

    option1 = client.post(
        "/api/v1/option/",
        json={"question_id": question1["id"], "option_text": "One"},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    option2 = client.post(
        "/api/v1/option/",
        json={"question_id": question2["id"], "option_text": "Two"},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()

    client.post(
        "/api/v1/vote/",
        json={"question_id": question1["id"], "option_id": option1["id"]},
        headers=auth_headers(token),
    )
    client.post(
        "/api/v1/vote/",
        json={"question_id": question2["id"], "option_id": option2["id"]},
        headers=auth_headers(token),
    )

    response = client.get(
        "/api/v1/user/me/stats",
        headers=auth_headers(token),
    )

    assert response.status_code == 200, response.json()
    assert response.json()["total_answers"] == 2
    assert response.json()["current_streak"] == 2
    assert response.json()["longest_streak"] == 2
