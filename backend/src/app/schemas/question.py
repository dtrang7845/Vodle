from datetime import datetime, date
from pydantic import BaseModel, ConfigDict

from app.schemas.option import OptionOut


class QuestionBase(BaseModel):
    title: str
    description: str | None = None
    question_text: str
    publish_date: date


class QuestionCreate(QuestionBase):
    pass


class QuestionOptionCreate(BaseModel):
    option_text: str


class QuestionCreateWithOptions(QuestionBase):
    options: list[QuestionOptionCreate]


class QuestionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    question_text: str | None = None
    publish_date: date | None = None


class QuestionOut(QuestionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionWithOptions(QuestionOut):
    options: list[OptionOut] = []

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
    publish_date: date
    created_at: datetime
    results: list[QuestionResultItem]

    model_config = ConfigDict(from_attributes=True)
