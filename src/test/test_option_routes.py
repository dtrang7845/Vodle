def create_question(
    client,
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
    )
    assert response.status_code == 201, response.json()
    return response.json()


def create_option(client, question_id, option_text="Blue"):
    response = client.post(
        "/api/v1/option/",
        json={
            "question_id": question_id,
            "option_text": option_text,
        },
    )
    assert response.status_code == 201, response.json()
    return response.json()


def test_create_option(client):
    question = create_question(client)

    data = create_option(client, question["id"], "Blue")

    assert "id" in data
    assert data["question_id"] == question["id"]
    assert data["option_text"] == "Blue"


def test_get_options(client):
    question = create_question(client)
    create_option(client, question["id"], "Blue")
    create_option(client, question["id"], "Red")

    response = client.get("/api/v1/option/")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_option_by_id(client):
    question = create_question(client)
    option = create_option(client, question["id"], "Blue")

    response = client.get(f"/api/v1/option/{option['id']}")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["id"] == option["id"]
    assert data["option_text"] == "Blue"


def test_get_option_not_found(client):
    response = client.get("/api/v1/option/999999")
    assert response.status_code == 404


def test_get_options_by_question(client):
    question = create_question(client)
    create_option(client, question["id"], "Blue")
    create_option(client, question["id"], "Red")

    response = client.get(f"/api/v1/option/question/{question['id']}")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(option["question_id"] == question["id"] for option in data)
