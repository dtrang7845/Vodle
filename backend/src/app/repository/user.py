from typing import TYPE_CHECKING
from sqlmodel import select

from app.models.user import User

if TYPE_CHECKING:
    from sqlmodel import Session


class UserRepository:
    @staticmethod
    def get_all(db: "Session") -> list[User]:
        statement = select(User)
        return db.exec(statement).all()

    @staticmethod
    def get_by_email(db: "Session", email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return db.exec(statement).first()

    @staticmethod
    def get_by_id(db: "Session", user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return db.exec(statement).first()

    @staticmethod
    def create(db: "Session", db_user: User) -> User:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update(db: "Session", db_user: User) -> User:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete(db: "Session", db_user: User) -> None:
        db.delete(db_user)
        db.commit()
