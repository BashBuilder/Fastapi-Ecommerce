from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import or_
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

    found_user = (
      self.db.query(models.User)
      .filter(
        or_(
          models.User.username == user_info["username"],
          models.User.email == user_info["email"],
        )
      )
      .first()
    )

    if found_user:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
      )

    new_user = models.User(**user_info)
    self.db.add(new_user)
    self.db.commit()
    self.db.refresh(new_user)

    return user_schema.UserOut.model_validate(new_user)

  async def get_user(self, id: UUID | str) -> user_schema.UserOut:
    user = self.db.query(models.User).filter(models.User.id == id).first()
    return user_schema.UserOut.model_validate(user)

  async def get_user_by_email(self, email: str) -> user_schema.UserOut:
    user = self.db.query(models.User).filter(models.User.email == email).first()
    return user_schema.UserOut.model_validate(user)

  async def update_user(
    self, id: UUID | str, payload: user_schema.UserUpdate
  ) -> user_schema.UserOut:
    user = self.db.query(models.User).filter(models.User.id == id).first()

    if not user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
      )

    user_update = models.User(**payload.model_dump())
    self.db.add(user_update)
    self.db.commit()
    self.db.refresh(user_update)

    return user_schema.UserOut.model_validate(user_update)
