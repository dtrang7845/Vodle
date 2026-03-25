from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.api.v1.routes import api_router
from app.core.database import engine

from app.core.settings import settings

# import all models cause they all work now


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


# SQLModel.metadata.create_all(engine)

app.include_router(api_router)
