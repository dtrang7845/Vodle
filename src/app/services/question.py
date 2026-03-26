from typing import TYPE_CHECKING, Counter

from app.models.question import Question
from app.repository.question import QuestionRepository
from app.repository.option import OptionRepository
from app.repository.vote import VoteRepository
from app.schemas.question import QuestionCreate, QuestionResultItem, QuestionWithResults, QuestionUpdate

from app.exceptions.notfound_excs import question_not_found_exception

if TYPE_CHECKING:
    from sqlmodel import Session


class QuestionService:
    def __init__(self) -> None:
        self.repository = QuestionRepository()
        self.option_repository = OptionRepository()
        self.vote_repository = VoteRepository()

    def get_all(self, db: "Session") -> list[Question]:
        return self.repository.get_all(db)

    def get_by_id(self, db: "Session", question_id: int) -> Question | None:
        return self.repository.get_by_id(db, question_id)

    def get_with_results(self, db: "Session", question_id: int) -> QuestionWithResults:
        db_question = self.repository.get_by_id(db, question_id)
        if not db_question:
            raise question_not_found_exception

        options = self.option_repository.get_by_question_id(db, question_id)
        votes = self.vote_repository.get_by_question_id(db, question_id)

        vote_counts = Counter(vote.option_id for vote in votes)

        results = [
            QuestionResultItem(
                option_id=option.id,
                option_text=option.option_text,
                votes=vote_counts.get(option.id, 0),
            )
            for option in options
            if option.id is not None
        ]

        return QuestionWithResults(
            id=db_question.id,
            title=db_question.title,
            description=db_question.description,
            question_text=db_question.question_text,
            created_at=db_question.created_at,
            results=results,
        )

    def create(self, db: "Session", question: QuestionCreate) -> Question:
        db_question = Question(**question.model_dump())
        return self.repository.create(db, db_question)
    
    def update(self, db: "Session", question_id: int, question: QuestionUpdate) -> Question:
        db_question = self.repository.get_by_id(db, question_id)
        if not db_question:
            raise question_not_found_exception
        return self.repository.update(db, db_question, question)

    def delete(self, db: "Session", question_id: int) -> None:
        db_question = self.repository.get_by_id(db, question_id)
        if not db_question:
            raise question_not_found_exception
        self.repository.delete(db, db_question)


question_service = QuestionService()
