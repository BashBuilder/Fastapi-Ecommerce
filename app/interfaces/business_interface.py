from abc import abstractmethod
from uuid import UUID

from app.schemas import business_schema


class IBusinessInterface:
  @abstractmethod
  async def create_business(
    self,
    payload: business_schema.BusinessCreate,
  ) -> business_schema.BusinessOut:
    pass

  @abstractmethod
  async def get_business(self, id: int) -> business_schema.BusinessOut:
    pass

  @abstractmethod
  async def get_business_by_owner_id(
    self, id: UUID | str
  ) -> business_schema.BusinessOut:
    pass

  @abstractmethod
  async def update_business(
    self,
    id: UUID | str,
    payload: business_schema.BusinessUpdate,
  ) -> business_schema.BusinessOut:
    pass
