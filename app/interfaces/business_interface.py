from abc import abstractmethod

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
