from typing import TYPE_CHECKING
from sqlmodel import select

from app.models.option import Option

if TYPE_CHECKING:
    from sqlmodel import Session


class OptionRepository:

    @staticmethod
    def get_all(db: "Session") -> list[Option]:
        statement = select(Option)
        return db.exec(statement).all()

    @staticmethod
    def get_by_id(db: "Session", option_id: int) -> Option | None:
        statement = select(Option).where(Option.id == option_id)
        return db.exec(statement).first()

    @staticmethod
    def get_by_question_id(db: "Session", question_id: int) -> list[Option]:
        statement = select(Option).where(Option.question_id == question_id)
        return db.exec(statement).all()

    @staticmethod
    def create(db: "Session", db_option: Option) -> Option:
        db.add(db_option)
        db.commit()
        db.refresh(db_option)
        return db_option

    @staticmethod
    def update(db: "Session", db_option: Option) -> Option:
        db.add(db_option)
        db.commit()
        db.refresh(db_option)
        return db_option

    @staticmethod
    def delete(db: "Session", db_option: Option) -> None:
        db.delete(db_option)
        db.commit()