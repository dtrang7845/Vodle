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
```
.
├── pyproject.toml
├── README.md
├── src
│ └── app
│ ├── init.py
│ ├── main.py
│ ├── api
│ │ └── v1
│ │ ├── init.py
│ │ └── routes.py
│ ├── core
│ │ ├── init.py
│ │ ├── authentication.py
│ │ ├── database.py
│ │ └── settings.py
│ ├── models
│ │ ├── init.py
│ │ ├── option.py
│ │ ├── question.py
│ │ ├── user.py
│ │ └── vote.py
│ ├── exceptions
│ │ ├── init.py
│ │ ├── login_excs.py
│ │ ├── notfound_excs.py
│ │ └── other_excs.py
│ ├── schemas
│ │ ├── init.py
│ │ ├── option.py
│ │ ├── question.py
│ │ ├── user.py
│ │ ├── vote.py
│ │ └── token.py
│ ├── services
│ │ ├── init.py
│ │ ├── option.py
│ │ ├── question.py
│ │ ├── user.py
│ │ └── vote.py
│ └── repository
│ ├── init.py
│ ├── option.py
│ ├── question.py
│ ├── user.py
│ └── vote.py
└── test
├── init.py
├── conftest.py
├── test_option_routes.py
├── test_question_routes.py
├── test_user_routes.py
└── test_vote_routes.py
```

## Setup Instructions
Note: Ensure that you have uv installed
1. Clone the repository
2. To create and sync the virtual environment
    - uv sync
    - source .venv/bin/activate (on macOS and Linux)
3. Run the server
    - uvicorn app.main:app --reload
    - uv run fastapi dev src/app/main.py
