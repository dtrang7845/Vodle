from __future__ import annotations

from datetime import date, timedelta

from sqlmodel import Session, select

from app.core.database import create_db_and_tables, engine
from app.models.question import Question
from app.schemas.question import QuestionCreateWithOptions
from app.services.question import question_service
from app.services.question_generation import question_generation_service


def seed_questions(days: int = 5) -> None:
    today = date.today()
    create_db_and_tables()

    with Session(engine) as session:
        used_question_texts = {
            question.question_text for question in session.exec(select(Question)).all()
        }

        for offset in range(days):
            publish_date = today + timedelta(days=offset)

            existing_question = session.exec(
                select(Question).where(Question.publish_date == publish_date)
            ).first()
            if existing_question is not None:
                print(f"Skipping {publish_date}: question already exists")
                continue

            draft = question_generation_service.generate_question_draft(
                used_question_texts=used_question_texts
            )
            created_question = question_service.create_with_options(
                session,
                QuestionCreateWithOptions(
                    title=draft.title,
                    description=draft.description,
                    question_text=draft.question_text,
                    publish_date=publish_date,
                    options=draft.options,
                ),
            )
            used_question_texts.add(created_question.question_text)
            print(f"Created question for {publish_date}: {created_question.title}")


if __name__ == "__main__":
    seed_questions()
