from __future__ import annotations

import argparse
from datetime import timedelta

from sqlmodel import Session, select

from app.core.dates import current_publish_date
from app.core.database import create_db_and_tables, engine
from app.models import option  # noqa: F401
from app.models.question import Question
from app.models import user  # noqa: F401
from app.models import vote  # noqa: F401
from app.schemas.question import QuestionCreateWithOptions
from app.services.question import question_service
from app.services.question_generation import question_generation_service


def generate_questions(
    days: int = 5, topic_hint: str | None = None, past_days: int = 0
) -> None:
    today = current_publish_date()
    create_db_and_tables()

    with Session(engine) as session:
        used_question_texts = {
            question.question_text for question in session.exec(select(Question)).all()
        }

        for offset in range(-max(past_days, 0), days):
            publish_date = today + timedelta(days=offset)

            existing_question = session.exec(
                select(Question).where(Question.publish_date == publish_date)
            ).first()
            if existing_question is not None:
                print(f"Skipping {publish_date}: question already exists")
                continue

            draft = question_generation_service.generate_question_draft(
                topic_hint=topic_hint,
                used_question_texts=used_question_texts,
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
            print(
                f"Created question-bank entry for {publish_date}: "
                f"{created_question.title}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Schedule daily questions from the local 300-question bank."
    )
    parser.add_argument(
        "--days",
        type=int,
        default=5,
        help="How many consecutive days of questions to generate",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Optional topic hint to steer generated questions",
    )
    parser.add_argument(
        "--past-days",
        type=int,
        default=0,
        help="How many previous days to backfill",
    )
    args = parser.parse_args()
    generate_questions(days=args.days, topic_hint=args.topic, past_days=args.past_days)
