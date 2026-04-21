from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import select

from app.models.question import Question

if TYPE_CHECKING:
    from sqlmodel import Session


class QuestionRepository:
    @staticmethod
    def get_all(db: "Session") -> list[Question]:
        statement = select(Question)
        return db.exec(statement).all()

    @staticmethod
    def get_by_id(db: "Session", question_id: int) -> Question | None:
        statement = select(Question).where(Question.id == question_id)
        return db.exec(statement).first()

    @staticmethod
    def get_today(db: "Session") -> Question | None:
        today = date.today()
        statement = select(Question).where(Question.publish_date == today)
        return db.exec(statement).first()

    @staticmethod
    def create(db: "Session", db_question: Question) -> Question:
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question

    @staticmethod
    def update(db: "Session", db_question: Question) -> Question:
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question

    @staticmethod
    def delete(db: "Session", db_question: Question) -> None:
        db.delete(db_question)
        db.commit()
