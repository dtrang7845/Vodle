# Voting Website Backend

This project is the backend for a full-stack voting web application built with:
**FastAPI**
**SQLModel**
**Pydantic**


## Features
- User Registration
- Create and manage voting requests
- Add options to questions
- Submit votes (one per question)
- Retrieve voting results according to question


## Project Structure

.
├── pyproject.toml
├── README.md
├── src
│   └── app
│       ├── __init__.py
│       ├── main.py
│       ├── api
│       │   └── v1
│       │       ├── __init__.py
│       │       └── routes.py
│       ├── core
│       │   ├── __init__.py
│       │   ├── authentication.py
│       │   ├── database.py
│       │   └── settings.py
│       ├── models
│       │   ├── __init__.py
│       │   ├── option.py
│       │   ├── question.py
│       │   └── user.py
│       │   └── vote.py
│       ├── exceptions
│       │   ├── __init__.py
│       │   ├── login_excs.py
│       │   ├── notfound_excs.py
│       │   └── other_excs.py
│       ├── schemas
│       │   ├── __init__.py
│       │   ├── option.py
│       │   ├── question.py
│       │   └── user.py
│       │   └── vote.py
│       │   └── token.py
│       ├── services
│       │   ├── __init__.py
│       │   ├── option.py
│       │   ├── question.py
│       │   └── user.py
│       │   └── vote.py
│       └── repository
│       │   ├── __init__.py
│       │   ├── option.py
│       │   ├── question.py
│       │   └── user.py
│       │   └── vote.py
└── └── test
        ├── __init__.py
        ├── conftest.py
        ├── test_option_routes.py
        ├── test_question_routes.py
        ├── test_user_routes.py
        ├── test_vote_routes.py
