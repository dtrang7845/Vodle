from __future__ import annotations

from sqlmodel import Session, select

from app.core.database import create_db_and_tables, engine
from app.models import option  # noqa: F401
from app.models import question  # noqa: F401
from app.models import vote  # noqa: F401
from app.models import user  # noqa: F401
from app.models.option import Option
from app.models.question import Question
from app.models.vote import Vote


def reset_question_data() -> None:
    create_db_and_tables()

    with Session(engine) as session:
        for db_vote in session.exec(select(Vote)).all():
            session.delete(db_vote)
        session.commit()

        for db_option in session.exec(select(Option)).all():
            session.delete(db_option)
        session.commit()

        for db_question in session.exec(select(Question)).all():
            session.delete(db_question)
        session.commit()

        print("Cleared all votes, options, and questions.")


if __name__ == "__main__":
    reset_question_data()
