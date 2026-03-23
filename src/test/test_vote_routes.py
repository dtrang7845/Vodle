# test/test_vote_routes.py

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


def create_question(client, title="Best color?", description="Choose one"):
    response = client.post(
        "/api/v1/question/",
        json={
            "title": title,
            "description": description,
        },
    )
    assert response.status_code == 201, response.json()
    return response.json()


def create_option(client, question_id, text="Blue"):
    response = client.post(
        "/api/v1/option/",
        json={
            "question_id": question_id,
            "text": text,
        },
    )
    assert response.status_code == 201, response.json()
    return response.json()


def create_vote(client, user_id, question_id, option_id):
    response = client.post(
        "/api/v1/vote/",
        json={
            "user_id": user_id,
            "question_id": question_id,
            "option_id": option_id,
        },
    )
    assert response.status_code == 201, response.json()
    return response.json()


def test_create_vote(client):
    user = create_user(client, "voter1")
    question = create_question(client)
    option = create_option(client, question["id"], "Blue")

    vote = create_vote(client, user["id"], question["id"], option["id"])

    assert "id" in vote
    assert vote["user_id"] == user["id"]
    assert vote["question_id"] == question["id"]
    assert vote["option_id"] == option["id"]


def test_get_votes(client):
    user = create_user(client, "voter1")
    question = create_question(client)
    option = create_option(client, question["id"], "Blue")
    create_vote(client, user["id"], question["id"], option["id"])

    response = client.get("/api/v1/vote/")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_vote_by_id(client):
    user = create_user(client, "voter1")
    question = create_question(client)
    option = create_option(client, question["id"], "Blue")
    vote = create_vote(client, user["id"], question["id"], option["id"])

    response = client.get(f"/api/v1/vote/{vote['id']}")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["id"] == vote["id"]
    assert data["user_id"] == user["id"]


def test_get_vote_not_found(client):
    response = client.get("/api/v1/vote/999999")
    assert response.status_code == 404


def test_create_vote_duplicate_same_user_same_question(client):
    user = create_user(client, "voter1")
    question = create_question(client)
    option = create_option(client, question["id"], "Blue")

    create_vote(client, user["id"], question["id"], option["id"])

    response = client.post(
        "/api/v1/vote/",
        json={
            "user_id": user["id"],
            "question_id": question["id"],
            "option_id": option["id"],
        },
    )

    assert response.status_code == 409, response.json()
    assert response.json()["detail"] == "User has already voted on this question"