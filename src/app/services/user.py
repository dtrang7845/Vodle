from typing import TYPE_CHECKING

from app.core.authentication import get_password_hash, verify_password
from app.models.user import User
from app.repository.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate

from app.exceptions.login_excs import (
    username_already_exists_exception,
    email_already_exists_exception,
)

from app.exceptions.notfound_excs import (
    user_not_found_exception,
)

if TYPE_CHECKING:
    from sqlmodel import Session


class UserService:
    def __init__(self) -> None:
        self.repository = UserRepository()

    def get_all(self, db: "Session") -> list[User]:
        return self.repository.get_all(db)

    def get_by_email(self, db: "Session", email: str) -> User | None:
        return self.repository.get_by_email(db, email)

    def get_by_username(self, db: "Session", username: str) -> User | None:
        return self.repository.get_by_username(db, username)

    def get_by_id(self, db: "Session", user_id: int) -> User | None:
        return self.repository.get_by_id(db, user_id)

    def is_email_exists(self, db: "Session", email: str) -> bool:
        return self.repository.get_by_email(db, email) is not None

    def is_username_exists(self, db: "Session", username: str) -> bool:
        return self.repository.get_by_username(db, username) is not None

    def create(self, db: "Session", user: UserCreate) -> User:
        existing_email = self.is_email_exists(db, user.email)
        if existing_email:
            raise email_already_exists_exception

        if self.is_username_exists(db, user.username):
            raise username_already_exists_exception

        db_user = User(
            username=user.username,
            email=user.email,
            password_hash=get_password_hash(user.password),
        )

        return self.repository.create(db, db_user)
    
    def update(self, db: "Session", user_id: int, user: UserUpdate) -> User:
        db_user = self.repository.get_by_id(db, user_id)
        if not db_user:
            raise user_not_found_exception
        return self.repository.update(db, db_user, user)

    def authenticate(self, db: "Session", email: str, password: str) -> User | None:
        user = self.repository.get_by_email(db, email)
        if user is None:
            return None

        if not verify_password(password, str(user.password_hash)):
            return None

        return user
    
    def delete(self, db: "Session", user_id: int) -> None:
        db_user = self.repository.get_by_id(db, user_id)
        if not db_user:
            raise user_not_found_exception
        self.repository.delete(db, db_user)


user_service = UserService()
