from datetime import date as calendar_date, timedelta
from typing import TYPE_CHECKING

from app.core.authentication import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.models.vote import Vote
from app.models.question import Question
from app.repository.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from sqlmodel import select

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
            role=UserRole.USER,
        )

        return self.repository.create(db, db_user)

    def update(self, db: "Session", user_id: int, user: UserUpdate) -> User:
        db_user = self.repository.get_by_id(db, user_id)
        if not db_user:
            raise user_not_found_exception

        db_user.password_hash = get_password_hash(user.password)
        return self.repository.update(db, db_user)

    def authenticate(self, db: "Session", email: str, password: str) -> User | None:
        user = self.repository.get_by_email(db, email)
        if user is None:
            return None

        if not verify_password(password, str(user.password_hash)):
            return None

        return user

    def get_stats(self, db: "Session", user_id: int) -> dict[str, int]:
        vote_dates = sorted(
            {
                publish_date
                for publish_date in db.exec(
                    select(Question.publish_date)
                    .join(Vote, Vote.question_id == Question.id)
                    .where(Vote.user_id == user_id)
                    .order_by(Question.publish_date)
                ).all()
            }
        )

        if not vote_dates:
            return {
                "total_answers": 0,
                "current_streak": 0,
                "longest_streak": 0,
            }

        longest_streak = 1
        running_streak = 1
        for previous_date, current_date in zip(vote_dates, vote_dates[1:]):
            if current_date == previous_date + timedelta(days=1):
                running_streak += 1
            else:
                longest_streak = max(longest_streak, running_streak)
                running_streak = 1

        longest_streak = max(longest_streak, running_streak)

        latest_vote_date = vote_dates[-1]
        if latest_vote_date < calendar_date.today() - timedelta(days=1):
            current_streak = 0
        else:
            current_streak = 1
            for index in range(len(vote_dates) - 1, 0, -1):
                if vote_dates[index] == vote_dates[index - 1] + timedelta(days=1):
                    current_streak += 1
                else:
                    break

        return {
            "total_answers": len(vote_dates),
            "current_streak": current_streak,
            "longest_streak": longest_streak,
        }

    def delete(self, db: "Session", user_id: int) -> None:
        db_user = self.repository.get_by_id(db, user_id)
        if not db_user:
            raise user_not_found_exception

        user_votes = db.exec(select(Vote).where(Vote.user_id == user_id)).all()
        for vote in user_votes:
            db.delete(vote)
        db.commit()

        self.repository.delete(db, db_user)


user_service = UserService()
