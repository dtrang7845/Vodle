from datetime import date


def create_question(
    client,
    admin_token,
    title="Best programming language?",
    description="Pick one",
    question_text="What is the best programming language?",
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


def test_create_question(client, admin_token):
    data = create_question(client, admin_token)

    assert "id" in data
    assert data["title"] == "Best programming language?"
    assert data["description"] == "Pick one"
    assert data["question_text"] == "What is the best programming language?"


def test_create_question_without_auth(client):
    response = client.post(
        "/api/v1/question/",
        json={
            "title": "Test",
            "question_text": "Test question?",
            "publish_date": date.today().isoformat(),
        },
    )
    assert response.status_code == 401


def test_get_questions(client, admin_token):
    create_question(client, admin_token)

    response = client.get("/api/v1/question/")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_question_by_id(client, admin_token):
    question = create_question(client, admin_token)

    response = client.get(f"/api/v1/question/{question['id']}")
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["id"] == question["id"]
    assert data["question_text"] == "What is the best programming language?"


def test_get_question_not_found(client):
    response = client.get("/api/v1/question/999999")
    assert response.status_code == 404


def test_update_question(client, admin_token):
    question = create_question(client, admin_token)

    response = client.put(
        f"/api/v1/question/{question['id']}",
        json={"title": "Updated title"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"


def test_update_question_not_found(client, admin_token):
    response = client.put(
        "/api/v1/question/999999",
        json={"title": "Updated title"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


def test_delete_question(client, admin_token):
    question = create_question(client, admin_token)

    response = client.delete(
        f"/api/v1/question/{question['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204


def test_delete_question_not_found(client, admin_token):
    response = client.delete(
        "/api/v1/question/999999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


def test_create_question_with_options(client, admin_token):
    response = client.post(
        "/api/v1/question/with-options",
        json={
            "title": "Best drink?",
            "description": "Pick one",
            "question_text": "Tea or coffee?",
            "publish_date": date.today().isoformat(),
            "options": [
                {"option_text": "Tea"},
                {"option_text": "Coffee"},
            ],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 201, response.json()
    data = response.json()
    assert data["question_text"] == "Tea or coffee?"
    assert len(data["options"]) == 2
