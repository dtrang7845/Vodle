from datetime import datetime
from pydantic import BaseModel, ConfigDict

class QuestionBase(BaseModel):
    title: str
    body: str | None = None
    
class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(QuestionBase):
    title: str | None = None
    body: str | None = None
    
class QuestionOut(QuestionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime