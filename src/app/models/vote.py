from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.question import Question
    from app.models.option import Option


class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    question_id: int = Field(foreign_key="question.id")
    option_id: int = Field(foreign_key="option.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # relationships
    user: "User" = Relationship(back_populates="votes")
    question: "Question" = Relationship(back_populates="votes")
    option: "Option" = Relationship(back_populates="votes")