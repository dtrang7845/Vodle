from typing import TYPE_CHECKING
from sqlmodel import create_engine
from sqlmodel.orm import Session, declarative_base,sessionmaker
from app.core.settings import settings

if TYPE_CHECKING:
    from collections.abc import Generator

engine = create_engine(settings.database.url,
                       connect_args = ({"check_same_thread": False}
        if settings.database_url.startswith("sqlite")
        else {}),
        )
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db() ->Generator[Session]:
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()