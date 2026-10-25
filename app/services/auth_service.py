from app.interfaces.business_interface import IBusinessInterface
from app.interfaces.user_interface import IUserInterface
from app.schemas import business_schema, user_schema


class AuthService:
  def __init__(self, user_repo: IUserInterface, business_repo: IBusinessInterface):
    self.user_repo = user_repo
    self.business_repo = business_repo

  async def register_user(self, payload: user_schema.UserCreate) -> user_schema.UserOut:
    new_user = await self.user_repo.create_user(payload)
    business_data = business_schema.BusinessCreate(
      name=new_user.username,
      owner_id=new_user.id,
    )

    await self.business_repo.create_business(business_data)

    return new_user
