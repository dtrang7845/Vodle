from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from sqlmodel import select, func

from app.models.question import Question
from app.models.option import Option
from app.models.vote import Vote
from app.repository.question import QuestionRepository
from app.schemas.question import (
    QuestionCreate,
    QuestionCreateWithOptions,
    QuestionWithResults,
    QuestionUpdate,
)

if TYPE_CHECKING:
    from sqlmodel import Session


class QuestionService:
    def __init__(self) -> None:
        self.repository = QuestionRepository()

    def get_all(self, db: "Session") -> list[Question]:
        return self.repository.get_all(db)

    def get_by_id(self, db: "Session", question_id: int) -> Question | None:
        return self.repository.get_by_id(db, question_id)

    def get_today(self, db: "Session") -> Question:
        question = self.repository.get_today(db)
        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No question found for today",
            )
        return question

    def get_with_results(
        self,
        db: "Session",
        question_id: int,
    ) -> QuestionWithResults:
        question = self.repository.get_by_id(db, question_id)
        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )

        options = db.exec(
            select(Option).where(Option.question_id == question_id).order_by(Option.id)
        ).all()

        vote_counts = {
            option_id: votes
            for option_id, votes in db.exec(
                select(Vote.option_id, func.count(Vote.id))
                .where(Vote.question_id == question_id)
                .group_by(Vote.option_id)
            ).all()
        }

        return QuestionWithResults(
            id=question.id,
            title=question.title,
            description=question.description,
            question_text=question.question_text,
            publish_date=question.publish_date,
            created_at=question.created_at,
            results=[
                {
                    "option_id": option.id,
                    "option_text": option.option_text,
                    "votes": vote_counts.get(option.id, 0),
                }
                for option in options
            ],
        )

    def create(self, db: "Session", question: QuestionCreate) -> Question:
        db_question = Question(**question.model_dump())
        return self.repository.create(db, db_question)

    def create_with_options(
        self,
        db: "Session",
        question: QuestionCreateWithOptions,
    ) -> Question:
        if len(question.options) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least two options are required",
            )

        db_question = Question(
            title=question.title,
            description=question.description,
            question_text=question.question_text,
            publish_date=question.publish_date,
        )
        db_question.options = [
            Option(option_text=option.option_text) for option in question.options
        ]

        return self.repository.create(db, db_question)

    def update(
        self,
        db: "Session",
        question_id: int,
        question: QuestionUpdate,
    ) -> Question:
        db_question = self.repository.get_by_id(db, question_id)
        if db_question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )

        question_data = question.model_dump(exclude_unset=True)
        for key, value in question_data.items():
            setattr(db_question, key, value)

        return self.repository.update(db, db_question)

    def delete(self, db: "Session", question_id: int) -> None:
        db_question = self.repository.get_by_id(db, question_id)
        if db_question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        self.repository.delete(db, db_question)


question_service = QuestionService()
