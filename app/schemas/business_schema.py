from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class BusinessBase(BaseModel):
  name: Annotated[str, Field(min_length=3, max_length=50)]
  city: str | None = None
  region: str | None = None
  description: str | None = None
  logo: str | None = None


class BusinessCreate(BusinessBase):
  owner_id: UUID


class BusinessOut(BusinessBase):
  id: UUID
  created_at: datetime
  updated_at: datetime
  owner_id: UUID

  class Config:
    from_attributes = True
