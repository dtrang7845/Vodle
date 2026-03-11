"""User schemas.

This module defines Pydantic schemas for user data validation and serialization.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


# -----------------------------
# Base
# -----------------------------

class UserBase(BaseModel):
    """Shared user fields."""

    email: EmailStr
    name: str


# -----------------------------
# Create
# -----------------------------

class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


# -----------------------------
# Response (what API returns)
# -----------------------------

class User(UserBase):
    """Schema for user response."""

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