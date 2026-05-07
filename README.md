# Vodle

A full-stack daily voting web application built with:
**Next.js** **FastAPI** **SQLModel** **Pydantic** **Docker**


## Features
- User registration and JWT authentication
- Daily question published each day with multiple choice options
- One vote per user per day with optional geolocation tagging
- Live results page with vote breakdowns and interactive 3D globe
- Voting history calendar with past answers and results
- User streaks and stats dashboard
- Dark / light theme toggle
- Admin panel for managing the question bank


## Project Structure
```
Voting-Website/
├── docker-compose.yaml
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── scripts/
│   │   ├── create_admin.py
│   │   ├── seed_daily_questions.py
│   │   ├── generate_daily_questions.py
│   │   └── reset_question_data.py
│   └── src/
│       └── app/
│           ├── __init__.py
│           ├── main.py
│           ├── api/
│           │   └── v1/
│           │       ├── __init__.py
│           │       └── routes.py
│           ├── core/
│           │   ├── __init__.py
│           │   ├── authentication.py
│           │   ├── database.py
│           │   ├── dates.py
│           │   └── settings.py
│           ├── models/
│           │   ├── __init__.py
│           │   ├── option.py
│           │   ├── question.py
│           │   ├── user.py
│           │   └── vote.py
│           ├── schemas/
│           │   ├── __init__.py
│           │   ├── option.py
│           │   ├── question.py
│           │   ├── token.py
│           │   ├── user.py
│           │   └── vote.py
│           ├── services/
│           │   ├── __init__.py
│           │   ├── option.py
│           │   ├── question.py
│           │   ├── question_generation.py
│           │   ├── user.py
│           │   └── vote.py
│           ├── repository/
│           │   ├── __init__.py
│           │   ├── option.py
│           │   ├── question.py
│           │   ├── user.py
│           │   └── vote.py
│           ├── exceptions/
│           │   ├── login_excs.py
│           │   ├── notfound_excs.py
│           │   └── other_excs.py
│           └── data/
│               └── question_bank.py
│       └── test/
│           ├── __init__.py
│           ├── conftest.py
│           ├── test_option_routes.py
│           ├── test_question_routes.py
│           ├── test_question_bank.py
│           ├── test_user_routes.py
│           └── test_vote_routes.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    └── src/
        ├── app/
        │   ├── layout.tsx
        │   ├── page.tsx
        │   ├── globals.css
        │   ├── (auth)/
        │   │   ├── layout.tsx
        │   │   ├── login/
        │   │   └── signup/
        │   ├── vote/
        │   ├── results/
        │   ├── history/
        │   ├── account/
        │   ├── settings/
        │   ├── admin/
        │   ├── about/
        │   └── user-stats/
        ├── components/
        │   ├── auth/
        │   │   ├── login-form.tsx
        │   │   └── signup-form.tsx
        │   ├── custom/
        │   │   ├── navbar.tsx
        │   │   ├── footer.tsx
        │   │   ├── vodle-logo.tsx
        │   │   ├── layout-shell.tsx
        │   │   ├── mode-toggle.tsx
        │   │   └── back-home-link.tsx
        │   └── ui/
        │       ├── globe.tsx
        │       ├── button.tsx
        │       ├── card.tsx
        │       ├── calendar.tsx
        │       └── input.tsx
        ├── lib/
        │   ├── api.ts
        │   ├── auth.ts
        │   ├── dates.ts
        │   ├── password-validation.ts
        │   ├── preferences.ts
        │   └── utils.ts
        └── test/
            ├── login-form.test.tsx
            ├── signup-form.test.tsx
            ├── vote.test.tsx
            ├── results.test.tsx
            ├── history.test.tsx
            ├── account.test.tsx
            └── e2e/
                └── vote-flow.spec.ts
```


## Setup Instructions
Note: Ensure that you have Docker Desktop, uv, and Bun installed

1. Clone the repository
2. Start the containers
    - `docker-compose up --build`
    - Backend runs at http://localhost:8000
    - Frontend runs at http://localhost:3000
3. Create an admin account
    - `docker-compose exec backend bash`
    - `uv run python scripts/create_admin.py --email admin@vodle.com --password YourPassword1!`
4. Open the app at http://localhost:3000

## Running Tests
Note: Run `bun install` inside `frontend/` before running tests for the first time
- Frontend unit tests: `cd frontend && bun run test`
- Frontend e2e tests: `cd frontend && bun run test:e2e`
- Backend: `cd backend && uv run pytest`
