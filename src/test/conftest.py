import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from app.core.database import get_db
from app.main import app

# Import models so metadata knows all tables


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_db_override():
        yield session

    app.dependency_overrides[get_db] = get_db_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="admin_token")
def admin_token_fixture(client: TestClient, session: Session) -> str:
    from app.models.user import User, UserRole
    from app.core.authentication import get_password_hash

    admin = User(
        username="admin",
        email="admin@test.com",
        password_hash=get_password_hash("admin123"),
        role=UserRole.ADMIN,
    )
    session.add(admin)
    session.commit()
    
    response = client.post(
        "/api/v1/user/login",
        data={"username": "admin@test.com", "password": "admin123"},
    )
    return response.json()["access_token"]
