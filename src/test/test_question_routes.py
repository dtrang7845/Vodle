def test_create_question(client):
    response = client.post(
        "/api/v1/question/",
        json={
            "title": "Best programming language?",
            "description": "Pick one",
        },
    )

    assert response.status_code == 201, response.json()
    data = response.json()
    assert "id" in data
    assert data["title"] == "Best programming language?"
    assert data["description"] == "Pick one"


def test_get_questions(client):
    create_response = client.post(
        "/api/v1/question/",
        json={
            "title": "Best programming language?",
            "description": "Pick one",
        },
    )
    assert create_response.status_code == 201, create_response.json()

    response = client.get("/api/v1/question/")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_question_by_id(client):
    create_response = client.post(
        "/api/v1/question/",
        json={
            "title": "Best programming language?",
            "description": "Pick one",
        },
    )
    assert create_response.status_code == 201, create_response.json()

    question_id = create_response.json()["id"]

    response = client.get(f"/api/v1/question/{question_id}")
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == question_id


def test_get_question_not_found(client):
    response = client.get("/api/v1/question/999999")
    assert response.status_code == 404