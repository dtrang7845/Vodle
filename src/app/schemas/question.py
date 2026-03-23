from datetime import datetime
from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    title: str
    description: str | None = None


class QuestionCreate(QuestionBase):
    pass


class QuestionOut(QuestionBase):
    id: int
    create_time: datetime

    model_config = ConfigDict(from_attributes=True)