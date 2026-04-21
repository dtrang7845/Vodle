from datetime import date


def create_user(client, username):
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


def login_user(client, email, password="secret123"):
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


def create_question(
    client,
    admin_token,
    title="Best color?",
    description="Choose one",
    question_text="What is your favorite color?",
    publish_date: str | None = None,
):
    response = client.post(
        "/api/v1/question/",
        json={
            "title": title,
            "description": description,
            "question_text": question_text,
            "publish_date": publish_date or date.today().isoformat(),
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201, response.json()
    return response.json()


def create_option(client, admin_token, question_id, option_text="Blue"):
    response = client.post(
        "/api/v1/option/",
        json={
            "question_id": question_id,
            "option_text": option_text,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201, response.json()
    return response.json()


def create_vote(client, token, question_id, option_id):
    response = client.post(
        "/api/v1/vote/",
        json={
            "question_id": question_id,
            "option_id": option_id,
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201, response.json()
    return response.json()


def test_create_vote(client, admin_token):
    user = create_user(client, "voter1")
    token = login_user(client, user["email"])["access_token"]
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")

    vote = create_vote(client, token, question["id"], option["id"])

    assert "id" in vote
    assert vote["user_id"] == user["id"]
    assert vote["question_id"] == question["id"]
    assert vote["option_id"] == option["id"]


def test_get_votes(client, admin_token):
    user = create_user(client, "voter1")
    token = login_user(client, user["email"])["access_token"]
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")
    create_vote(client, token, question["id"], option["id"])

    response = client.get("/api/v1/vote/")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_vote_by_id(client, admin_token):
    user = create_user(client, "voter1")
    token = login_user(client, user["email"])["access_token"]
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")
    vote = create_vote(client, token, question["id"], option["id"])

    response = client.get(f"/api/v1/vote/{vote['id']}")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["id"] == vote["id"]
    assert data["user_id"] == user["id"]


def test_get_vote_not_found(client):
    response = client.get("/api/v1/vote/999999")
    assert response.status_code == 404


def test_create_vote_duplicate_same_user_same_question(client, admin_token):
    user = create_user(client, "voter1")
    token = login_user(client, user["email"])["access_token"]
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")

    create_vote(client, token, question["id"], option["id"])

    response = client.post(
        "/api/v1/vote/",
        json={
            "question_id": question["id"],
            "option_id": option["id"],
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 409, response.json()
    assert response.json()["detail"] == "User has already voted on this question"


def test_create_vote_without_auth(client, admin_token):
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")

    response = client.post(
        "/api/v1/vote/",
        json={
            "question_id": question["id"],
            "option_id": option["id"],
        },
    )

    assert response.status_code == 401


def test_update_vote(client, admin_token):
    user = create_user(client, "voter1")
    token = login_user(client, user["email"])["access_token"]
    question = create_question(client, admin_token)
    option1 = create_option(client, admin_token, question["id"], "Blue")
    option2 = create_option(client, admin_token, question["id"], "Red")
    vote = create_vote(client, token, question["id"], option1["id"])

    response = client.put(
        f"/api/v1/vote/{vote['id']}",
        json={"option_id": option2["id"]},
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    assert response.json()["option_id"] == option2["id"]


def test_delete_vote(client, admin_token):
    user = create_user(client, "voter1")
    token = login_user(client, user["email"])["access_token"]
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")
    vote = create_vote(client, token, question["id"], option["id"])

    response = client.delete(
        f"/api/v1/vote/{vote['id']}",
        headers=auth_headers(token),
    )
    assert response.status_code == 204


def test_delete_vote_unauthorized(client, admin_token):
    user1 = create_user(client, "voter1")
    user2 = create_user(client, "voter2")
    token1 = login_user(client, user1["email"])["access_token"]
    token2 = login_user(client, user2["email"])["access_token"]
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")
    vote = create_vote(client, token1, question["id"], option["id"])

    response = client.delete(
        f"/api/v1/vote/{vote['id']}",
        headers=auth_headers(token2),
    )
    assert response.status_code == 403
