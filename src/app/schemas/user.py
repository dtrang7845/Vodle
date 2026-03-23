from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# -----------------------------
# Base
# -----------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr


# -----------------------------
# Create (input)
# -----------------------------
class UserCreate(UserBase):
    password: str


# -----------------------------
# Response (output)
# -----------------------------
class UserOut(UserBase):
    id: int
    create_time: datetime

    model_config = ConfigDict(from_attributes=True)