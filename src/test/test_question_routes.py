def create_question(
    client,
    title="Best programming language?",
    description="Pick one",
    question_text="What is the best programming language?",
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


def test_create_question(client):
    data = create_question(client)

    assert "id" in data
    assert data["title"] == "Best programming language?"
    assert data["description"] == "Pick one"
    assert data["question_text"] == "What is the best programming language?"


def test_get_questions(client):
    create_question(client)

    response = client.get("/api/v1/question/")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_question_by_id(client):
    question = create_question(client)

    response = client.get(f"/api/v1/question/{question['id']}")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["id"] == question["id"]
    assert data["question_text"] == "What is the best programming language?"


def test_get_question_not_found(client):
    response = client.get("/api/v1/question/999999")
    assert response.status_code == 404
