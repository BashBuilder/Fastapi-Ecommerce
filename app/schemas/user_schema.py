from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
  username: str
  email: str


class UserCreate(UserBase):
  password: str


class UserOut(UserBase):
  id: UUID
  join_date: datetime
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True
