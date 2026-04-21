from datetime import UTC, datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.question import Question
    from app.models.option import Option


class Vote(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="unique_vote_user_question"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True)
    question_id: int = Field(foreign_key="question.id", index=True)
    option_id: int = Field(foreign_key="option.id", index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    user: "User" = Relationship(back_populates="votes")
    question: "Question" = Relationship(back_populates="votes")
    option: "Option" = Relationship(back_populates="votes")
