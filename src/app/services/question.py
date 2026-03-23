from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from app.models.question import Question
from app.repository.question import QuestionRepository
from app.schemas.question import QuestionCreate

if TYPE_CHECKING:
    from sqlmodel import Session


class QuestionService:
    def __init__(self) -> None:
        self.repository = QuestionRepository()

    def get_all(self, db: "Session") -> list[Question]:
        return self.repository.get_all(db)

    def get_by_id(self, db: "Session", question_id: int) -> Question | None:
        return self.repository.get_by_id(db, question_id)

    def create(self, db: "Session", question: QuestionCreate) -> Question:
        db_question = Question(**question.model_dump())
        return self.repository.create(db, db_question)

    def delete(self, db: "Session", question_id: int) -> None:
        db_question = self.repository.get_by_id(db, question_id)
        if not db_question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        self.repository.delete(db, db_question)


question_service = QuestionService()