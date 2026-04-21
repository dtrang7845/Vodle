from __future__ import annotations

from datetime import date, timedelta

from sqlmodel import Session, select

from app.core.database import create_db_and_tables, engine
from app.models import vote  # noqa: F401
from app.models.option import Option
from app.models.question import Question
from app.models.user import User  # noqa: F401


SEED_QUESTIONS = [
    {
        "title": "Morning Ritual",
        "description": "A light opener for the day.",
        "question_text": "How do you prefer to start your morning?",
        "options": ["Coffee", "Tea", "Water"],
    },
    {
        "title": "Work Style",
        "description": "A quick pulse on productivity habits.",
        "question_text": "Which work style suits you best?",
        "options": ["Deep focus", "Collaborative sessions", "Short sprints"],
    },
    {
        "title": "Travel Pace",
        "description": "Vacation energy check.",
        "question_text": "When traveling, what pace do you enjoy most?",
        "options": ["Packed itinerary", "Balanced mix", "Slow and flexible"],
    },
    {
        "title": "Music While Working",
        "description": "Background sound preferences.",
        "question_text": "What do you listen to while working?",
        "options": ["Silence", "Instrumental", "Lyrics and playlists"],
    },
    {
        "title": "Weekend Plan",
        "description": "A simple end-of-week question.",
        "question_text": "What sounds best for this weekend?",
        "options": ["Stay in", "Go out", "A bit of both"],
    },
]


def seed_questions(days: int = 5) -> None:
    today = date.today()
    create_db_and_tables()

    with Session(engine) as session:
        for offset in range(days):
            publish_date = today + timedelta(days=offset)

            existing_question = session.exec(
                select(Question).where(Question.publish_date == publish_date)
            ).first()
            if existing_question is not None:
                print(f"Skipping {publish_date}: question already exists")
                continue

            template = SEED_QUESTIONS[offset % len(SEED_QUESTIONS)]
            question = Question(
                title=template["title"],
                description=template["description"],
                question_text=template["question_text"],
                publish_date=publish_date,
            )
            session.add(question)
            session.commit()
            session.refresh(question)

            for option_text in template["options"]:
                session.add(Option(option_text=option_text, question_id=question.id))

            session.commit()
            print(f"Created question for {publish_date}: {question.title}")


if __name__ == "__main__":
    seed_questions()
