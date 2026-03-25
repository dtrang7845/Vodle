from datetime import UTC, datetime
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.question import Question
    from app.models.vote import Vote


class Option(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    option_text: str
    question_id: int = Field(foreign_key="question.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # relationships
    question: "Question" = Relationship(back_populates="options")
    votes: List["Vote"] = Relationship(back_populates="option")