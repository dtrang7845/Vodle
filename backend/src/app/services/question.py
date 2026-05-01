from datetime import timedelta
from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from sqlmodel import select, func

from app.core.dates import current_publish_date
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
from app.services.question_generation import question_generation_service

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

    def ensure_scheduled_questions(
        self, db: "Session", future_days: int, past_days: int = 0
    ) -> int:
        future_days = max(future_days, 1)
        past_days = max(past_days, 0)
        today = current_publish_date()
        created_count = 0
        used_question_texts = {
            question.question_text for question in db.exec(select(Question)).all()
        }

        for offset in range(-past_days, future_days):
            publish_date = today + timedelta(days=offset)
            existing_question = db.exec(
                select(Question).where(Question.publish_date == publish_date)
            ).first()
            if existing_question is not None:
                continue

            draft = question_generation_service.generate_question_draft(
                used_question_texts=used_question_texts
            )
            created_question = self.create_with_options(
                db,
                QuestionCreateWithOptions(
                    title=draft.title,
                    description=draft.description,
                    question_text=draft.question_text,
                    publish_date=publish_date,
                    options=draft.options,
                ),
            )
            used_question_texts.add(created_question.question_text)
            created_count += 1

        return created_count

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
        vote_locations = db.exec(
            select(Vote.latitude, Vote.longitude, Vote.country, func.count(Vote.id))
            .where(
                Vote.question_id == question_id,
                Vote.latitude.is_not(None),
                Vote.longitude.is_not(None),
            )
            .group_by(Vote.latitude, Vote.longitude, Vote.country)
        ).all()

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
            vote_locations=[
                {
                    "latitude": latitude,
                    "longitude": longitude,
                    "country": country,
                    "votes": votes,
                }
                for latitude, longitude, country, votes in vote_locations
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
