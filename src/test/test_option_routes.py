def create_question(
    client,
    admin_token,
    title="Best color?",
    description="Choose one",
    question_text="What is your favorite color?",
):
    response = client.post(
        "/api/v1/question/",
        json={
            "title": title,
            "description": description,
            "question_text": question_text,
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


def test_create_option(client, admin_token):
    question = create_question(client, admin_token)

    data = create_option(client, admin_token, question["id"], "Blue")

    assert "id" in data
    assert data["question_id"] == question["id"]
    assert data["option_text"] == "Blue"


def test_get_options(client, admin_token):
    question = create_question(client, admin_token)
    create_option(client, admin_token, question["id"], "Blue")
    create_option(client, admin_token, question["id"], "Red")

    response = client.get("/api/v1/option/")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_option_by_id(client, admin_token):
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")

    response = client.get(f"/api/v1/option/{option['id']}")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["id"] == option["id"]
    assert data["option_text"] == "Blue"


def test_get_option_not_found(client):
    response = client.get("/api/v1/option/999999")
    assert response.status_code == 404


def test_get_options_by_question(client, admin_token):
    question = create_question(client, admin_token)
    create_option(client, admin_token, question["id"], "Blue")
    create_option(client, admin_token, question["id"], "Red")

    response = client.get(f"/api/v1/option/question/{question['id']}")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(option["question_id"] == question["id"] for option in data)


def test_update_option(client, admin_token):
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")

    response = client.put(
        f"/api/v1/option/{option['id']}",
        json={
            "option_text": "Red",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200, response.json()
    assert response.json()["option_text"] == "Red"


def test_delete_option(client, admin_token):
    question = create_question(client, admin_token)
    option = create_option(client, admin_token, question["id"], "Blue")

    response = client.delete(
        f"/api/v1/option/{option['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204


def test_create_option_without_auth(client, admin_token):
    question = create_question(client, admin_token)

    response = client.post(
        "/api/v1/option/",
        json={"question_id": question["id"], "option_text": "Blue"},
    )
    assert response.status_code == 401
