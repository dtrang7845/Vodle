from datetime import datetime
from pydantic import BaseModel, ConfigDict

class OptionBase(BaseModel):
    text: str
    
class OptionCreate(OptionBase):
    question_id: int
    
class OptionUpdate(OptionBase):
    text: str | None = None
    
class OptionOut(OptionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    question_id: int
    created_at: datetime