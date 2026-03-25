from datetime import UTC, datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.option import Option
    from app.models.vote import Vote

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    question_text: str
    
    options: List["Option"] = Relationship(back_populates="question")
    votes: List["Vote"] = Relationship(back_populates="question")