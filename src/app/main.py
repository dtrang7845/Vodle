from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.api.v1.routes import api_router
from app.core.database import engine

from app.models.user import User
from app.models.question import Question
from app.models.option import Option
from app.models.vote import Vote

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLModel.metadata.create_all(engine)

app.include_router(api_router)