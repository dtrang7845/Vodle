from typing import TYPE_CHECKING
from sqlmodel import select

from app.models.vote import Vote

if TYPE_CHECKING:
    from sqlmodel import Session


class VoteRepository:

    @staticmethod
    def get_all(db: "Session") -> list[Vote]:
        statement = select(Vote)
        return db.exec(statement).all()

    @staticmethod
    def get_by_id(db: "Session", vote_id: int) -> Vote | None:
        statement = select(Vote).where(Vote.id == vote_id)
        return db.exec(statement).first()

    @staticmethod
    def get_by_question_id(db: "Session", question_id: int) -> list[Vote]:
        statement = select(Vote).where(Vote.question_id == question_id)
        return db.exec(statement).all()

    @staticmethod
    def get_existing_vote(
        db: "Session", user_id: int, question_id: int
    ) -> Vote | None:
        statement = select(Vote).where(
            Vote.user_id == user_id,
            Vote.question_id == question_id,
        )
        return db.exec(statement).first()

    @staticmethod
    def create(db: "Session", db_vote: Vote) -> Vote:
        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)
        return db_vote

    @staticmethod
    def update(db: "Session", db_vote: Vote) -> Vote:
        db.commit()
        db.refresh(db_vote)
        return db_vote

    @staticmethod
    def delete(db: "Session", db_vote: Vote) -> None:
        db.delete(db_vote)
        db.commit()