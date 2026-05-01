from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import Session

from app.api.v1.routes import api_router
from app.core.database import create_db_and_tables, engine
from app.services.question import question_service

from app.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    if settings.auto_seed_daily_questions:
        with Session(engine) as session:
            question_service.ensure_scheduled_questions(
                session,
                future_days=settings.scheduled_question_days,
                past_days=settings.archived_question_days,
            )
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    print(f"{request.method} {request.url.path} -> {response.status_code}")
    return response


app.include_router(api_router)
