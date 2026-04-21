from typing import TYPE_CHECKING

from app.models.option import Option
from app.repository.option import OptionRepository
from app.repository.question import QuestionRepository
from app.schemas.option import OptionCreate, OptionUpdate

from app.exceptions.notfound_excs import (
    question_not_found_exception,
    option_not_found_exception,
)

if TYPE_CHECKING:
    from sqlmodel import Session


class OptionService:
    def __init__(self) -> None:
        self.repository = OptionRepository()
        self.question_repository = QuestionRepository()

    def get_all(self, db: "Session") -> list[Option]:
        return self.repository.get_all(db)

    def get_by_id(self, db: "Session", option_id: int) -> Option | None:
        return self.repository.get_by_id(db, option_id)

    def get_by_question_id(self, db: "Session", question_id: int) -> list[Option]:
        db_question = self.question_repository.get_by_id(db, question_id)
        if not db_question:
            raise question_not_found_exception
        return self.repository.get_by_question_id(db, question_id)

    def create(self, db: "Session", option: OptionCreate) -> Option:
        db_question = self.question_repository.get_by_id(db, option.question_id)
        if not db_question:
            raise question_not_found_exception

        db_option = Option(**option.model_dump())
        return self.repository.create(db, db_option)

    def update(self, db: "Session", option_id: int, option: OptionUpdate) -> Option:
        db_option = self.repository.get_by_id(db, option_id)
        if not db_option:
            raise option_not_found_exception

        update_data = option.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_option, key, value)

        return self.repository.update(db, db_option)

    def delete(self, db: "Session", option_id: int) -> None:
        db_option = self.repository.get_by_id(db, option_id)
        if not db_option:
            raise option_not_found_exception
        self.repository.delete(db, db_option)


option_service = OptionService()
