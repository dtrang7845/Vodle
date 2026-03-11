"""User schemas.

This module defines Pydantic schemas for user data validation and serialization.
"""

from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Base
# -----------------------------

class QuestionBase(BaseModel):
    """Shared question fields."""

    title: str
    description: str


# -----------------------------
# Create
# -----------------------------

class QuestionCreate(QuestionBase):
    """Schema for creating a new question."""

    questionID: int 
    create_time: datetime


# -----------------------------
# Response (what API returns)
# -----------------------------

class Question(QuestionBase):
    """Schema for question response."""

    id: int  
    create_time: datetime

    model_config = {"from_attributes": True}


# -----------------------------
# Auth Token
# -----------------------------

class Token(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    token_type: str