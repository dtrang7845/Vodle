from typing import TYPE_CHECKING

from app.models.vote import Vote
from app.repository.vote import VoteRepository
from app.repository.user import UserRepository
from app.repository.question import QuestionRepository
from app.repository.option import OptionRepository
from app.schemas.vote import VoteCreate

from app.exceptions.notfound_excs import (
    vote_not_found_exception,
    question_not_found_exception,
    option_not_found_exception,
)
from app.exceptions.other_excs import (
    user_already_voted_exception, 
    bad_option_exception,
    user_vote_deletion_exception,
)

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
            raise question_not_found_exception
        return self.repository.get_by_question_id(db, question_id)

    def create(self, db: "Session", vote: VoteCreate, user_id: int) -> Vote:
        db_question = self.question_repository.get_by_id(db, vote.question_id)
        if db_question is None:
            raise question_not_found_exception

        db_option = self.option_repository.get_by_id(db, vote.option_id)
        if db_option is None:
            raise option_not_found_exception

        if db_option.question_id != vote.question_id:
            raise bad_option_exception

        existing_vote = self.repository.get_existing_vote(db, user_id, vote.question_id)
        if existing_vote is not None:
            raise user_already_voted_exception

        db_vote = Vote(
            user_id=user_id,
            question_id=vote.question_id,
            option_id=vote.option_id,
        )
        return self.repository.create(db, db_vote)

    def delete(self, db: "Session", vote_id: int, current_user_id: int) -> None:
        db_vote = self.repository.get_by_id(db, vote_id)
        if db_vote is None:
            raise vote_not_found_exception
        if db_vote.user_id != current_user_id:
            raise user_vote_deletion_exception
        self.repository.delete(db, db_vote)


vote_service = VoteService()
