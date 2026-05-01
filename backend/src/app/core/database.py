from collections.abc import Generator
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlmodel import SQLModel, Session, create_engine

from app.core.settings import settings


def _ensure_sqlite_parent_dir(database_url: str) -> None:
    url = make_url(database_url)
    if url.drivername != "sqlite" or not url.database:
        return

    if url.database == ":memory:":
        return

    Path(url.database).expanduser().parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_parent_dir(settings.database_url)

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    if settings.database_url.startswith("sqlite"):
        with engine.begin() as connection:
            columns = {
                row[1] for row in connection.exec_driver_sql("PRAGMA table_info(vote)")
            }
            migrations = {
                "latitude": "ALTER TABLE vote ADD COLUMN latitude FLOAT",
                "longitude": "ALTER TABLE vote ADD COLUMN longitude FLOAT",
                "country": "ALTER TABLE vote ADD COLUMN country VARCHAR",
            }
            for column, statement in migrations.items():
                if column not in columns:
                    connection.execute(text(statement))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
