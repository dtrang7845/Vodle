from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from app.models.vote import Vote
from app.repository.vote import VoteRepository
from app.repository.user import UserRepository
from app.repository.question import QuestionRepository
from app.repository.option import OptionRepository
from app.schemas.vote import VoteCreate

if TYPE_CHECKING:
    from sqlmodel import Session


class VoteService:
    def __init__(self) -> None:
        self.repository = VoteRepository()
        self.user_repository = UserRepository()
        self.question_repository = QuestionRepository()
        self.option_repository = OptionRepository()

    def get_all(self, db: "Session") -> list[Vote]:
        return self.repository.get_all(db)

    def get_by_id(self, db: "Session", vote_id: int) -> Vote | None:
        return self.repository.get_by_id(db, vote_id)

    def get_by_question_id(self, db: "Session", question_id: int) -> list[Vote]:
        db_question = self.question_repository.get_by_id(db, question_id)
        if not db_question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        return self.repository.get_by_question_id(db, question_id)

    def create(self, db: "Session", vote: VoteCreate) -> Vote:
        db_user = self.user_repository.get_by_id(db, vote.user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        db_question = self.question_repository.get_by_id(db, vote.question_id)
        if not db_question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )

        db_option = self.option_repository.get_by_id(db, vote.option_id)
        if not db_option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Option not found",
            )

        if db_option.question_id != vote.question_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Option does not belong to this question",
            )

        existing_vote = self.repository.get_existing_vote(
            db, vote.user_id, vote.question_id
        )
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already voted on this question",
            )

        db_vote = Vote(**vote.model_dump())
        return self.repository.create(db, db_vote)

    def delete(self, db: "Session", vote_id: int) -> None:
        db_vote = self.repository.get_by_id(db, vote_id)
        if not db_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote not found",
            )
        self.repository.delete(db, db_vote)


vote_service = VoteService()