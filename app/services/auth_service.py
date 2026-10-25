from app.interfaces.user_repository import IUserRepository
from app.schemas import user_schema


class AuthService:
  def __init__(self, user_repo: IUserRepository):
    self.user_repo = user_repo

  async def register_user(self, payload: user_schema.UserCreate) -> user_schema.UserOut:
    return await self.user_repo.create_user(payload)
