from sqlalchemy.orm import Session

from app.interfaces.business_interface import IBusinessInterface
from app.models.sqlalchemy import models
from app.schemas import business_schema


class BusinessRepository(IBusinessInterface):
  def __init__(self, db: Session):
    self.db = db

  async def create_business(
    self,
    payload: business_schema.BusinessCreate,
  ) -> business_schema.BusinessOut:
    business_info = payload.model_dump()
    new_business = models.Business(**business_info)
    self.db.add(new_business)
    self.db.commit()
    self.db.refresh(new_business)

    return business_schema.BusinessOut.model_validate(new_business)

  async def get_business(self, id: int) -> business_schema.BusinessOut:
    business = self.db.query(models.Business).filter(models.Business.id == id).first()
    return business_schema.BusinessOut.model_validate(business)
