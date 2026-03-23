from datetime import datetime
from pydantic import BaseModel, ConfigDict


class OptionBase(BaseModel):
    text: str


class OptionCreate(OptionBase):
    question_id: int


class OptionOut(OptionBase):
    id: int
    question_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)