from datetime import datetime
from pydantic import BaseModel, ConfigDict


class OptionBase(BaseModel):
    option_text: str


class OptionCreate(OptionBase):
    question_id: int
    option_text: str


class OptionOut(OptionBase):
    id: int
    question_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)