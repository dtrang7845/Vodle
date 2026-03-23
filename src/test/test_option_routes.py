def test_create_option(client):
    question_response = client.post(
        "/api/v1/question/",
        json={
            "title": "Best color?",
            "description": "Choose one",
        },
    )
    assert question_response.status_code == 201, question_response.json()
    question_id = question_response.json()["id"]

    response = client.post(
        "/api/v1/option/",
        json={
            "question_id": question_id,
            "text": "Blue",
        },
    )

    assert response.status_code == 201, response.json()
    data = response.json()
    assert "id" in data, data