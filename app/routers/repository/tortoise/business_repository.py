from uuid import UUID

from fastapi import HTTPException, status

from app.interfaces.business_interface import IBusinessInterface
from app.models.tortoise.business import Business
from app.schemas import business_schema


class TBusinessRepository(IBusinessInterface):
  def __init__(
    self,
  ):
    pass

  async def create_business(
    self,
    payload: business_schema.BusinessCreate,
  ) -> business_schema.BusinessOut:
    found_business = await Business.get_or_none(name=payload.name)

    if found_business:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Business already exists"
      )

    business_obj = await Business.create(**payload.model_dump())

    return business_schema.BusinessOut.model_validate(business_obj)

  async def get_business(
    self,
    id: int,
  ) -> business_schema.BusinessOut:

    business_obj = await Business.get_or_none(id=id)

    if business_obj is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Business not found"
      )

    return business_schema.BusinessOut.model_validate(business_obj)

  async def get_business_by_owner_id(
    self,
    id: UUID | str,
  ) -> business_schema.BusinessOut:
    business_obj = await Business.get_or_none(owner_id=id)

    if business_obj is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Business not found"
      )

    return business_schema.BusinessOut.model_validate(business_obj)

  async def update_business(
    self,
    id: UUID | str,
    payload: business_schema.BusinessUpdate,
  ) -> business_schema.BusinessOut:
    business_obj = await Business.get_or_none(id=id)

    if business_obj is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Business not found"
      )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
      setattr(business_obj, field, value)

    await business_obj.save()

    return business_schema.BusinessOut.model_validate(business_obj)
