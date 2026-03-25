from datetime import datetime
from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    title: str
    description: str | None = None


class QuestionCreate(QuestionBase):
    question_text: str


class QuestionOut(QuestionBase):
    id: int
    question_text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionResultItem(BaseModel):
    option_id: int
    option_text: str
    votes: int


class QuestionWithResults(BaseModel):
    id: int
    title: str
    description: str | None = None
    question_text: str
    created_at: datetime
    results: list[QuestionResultItem]

    model_config = ConfigDict(from_attributes=True)
