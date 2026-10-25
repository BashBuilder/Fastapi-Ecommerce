from sqlalchemy.orm import Session

from app.interfaces.user_interface import IUserInterface
from app.models.sqlalchemy import models
from app.schemas import user_schema
from app.utils.auth import hash_password


class UserRepository(IUserInterface):
  def __init__(self, db: Session):
    self.db = db

  async def create_user(self, payload: user_schema.UserCreate) -> user_schema.UserOut:
    user_info = payload.model_dump()
    user_info["password"] = hash_password(user_info["password"])

    new_user = models.User(**user_info)
    self.db.add(new_user)
    self.db.commit()
    self.db.refresh(new_user)

    return user_schema.UserOut.model_validate(new_user)

  async def get_user(self, id: int) -> user_schema.UserOut:
    user = self.db.query(models.User).filter(models.User.id == id).first()
    return user_schema.UserOut.model_validate(user)

  async def get_user_by_email(self, email: str) -> user_schema.UserOut:
    user = self.db.query(models.User).filter(models.User.email == email).first()
    return user_schema.UserOut.model_validate(user)
