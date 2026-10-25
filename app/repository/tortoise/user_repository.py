from app.interfaces.user_repository import IUserRepository
from app.models.tortoise import user
from app.schemas import user_schema
from app.utils.auth import hash_password


class TUserRepository(IUserRepository):
  def __init__(self):
    pass

  async def create_user(self, payload: user_schema.UserCreate) -> user_schema.UserOut:
    user_info = payload.model_dump()
    user_info["password"] = hash_password(user_info["password"])
    user_obj = await user.User.create(**user_info)
    new_user = await user.user_pydantic.from_tortoise_orm(user_obj)

    return user_schema.UserOut.model_validate(new_user)

  async def get_user(self, id: int) -> user_schema.UserOut:
    found_user = await user.User.get(id=id)
    return user_schema.UserOut.model_validate(found_user)

  async def get_user_by_email(self, email: str) -> user_schema.UserOut:
    found_user = await user.User.get(email=email)
    return user_schema.UserOut.model_validate(found_user)
