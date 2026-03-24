from datetime import datetime
from pydantic import BaseModel, ConfigDict


class VoteCreate(BaseModel):
    question_id: int
    option_id: int


class VoteOut(BaseModel):
    id: int
    user_id: int
    question_id: int
    option_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)