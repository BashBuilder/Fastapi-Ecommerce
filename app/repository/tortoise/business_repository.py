from fastapi import HTTPException, status

from app.interfaces.business_interface import IBusinessInterface
from app.models.tortoise.business import Business
from app.schemas import business_schema


class TBusinessRepository(IBusinessInterface):
  def __init__(self, business_model: type[Business] = Business):
    self.business_model = business_model

  async def create_business(
    self,
    payload: business_schema.BusinessCreate,
  ) -> business_schema.BusinessOut:

    business_obj = await self.business_model.create(**payload.model_dump())

    return business_schema.BusinessOut.model_validate(business_obj)

  async def get_business(
    self,
    id: int,
  ) -> business_schema.BusinessOut:

    business_obj = await self.business_model.get_or_none(id=id)

    if business_obj is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Business not found"
      )

    return business_schema.BusinessOut.model_validate(business_obj)
