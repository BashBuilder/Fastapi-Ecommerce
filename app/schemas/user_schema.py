from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator
from zxcvbn import zxcvbn


class UserBase(BaseModel):
  username: Annotated[str, Field(min_length=3, max_length=50)]
  email: EmailStr


class UserCreate(UserBase):
  password: Annotated[str, Field(min_length=8, max_length=128)]

  @field_validator("username")
  @classmethod
  def validate_username(cls, value: str) -> str:
    if not value.strip():
      raise ValueError("Username cannot be empty")

    return value.strip()

  @field_validator("password")
  @classmethod
  def validate_password(cls, value: str) -> str:
    if not value.strip():
      raise ValueError("Password cannot be empty")

    result = zxcvbn(value)
    print("Score:", result["score"])
    print("Warning:", result["feedback"]["warning"])
    print("Suggestions:", result["feedback"]["suggestions"])
    print("Patterns:", result["sequence"])

    if result["score"] < 3:
      raise ValueError("Password is too weak. Choose a stronger password.")

    return value


class UserOut(UserBase):
  id: UUID
  join_date: datetime
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True
