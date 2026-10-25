from abc import abstractmethod

from app.schemas import user_schema


class IUserRepository:
  @abstractmethod
  async def create_user(self, payload: user_schema.UserCreate) -> user_schema.UserOut:
    pass

  @abstractmethod
  async def get_user(self, id: int) -> user_schema.UserOut | None:
    pass

  @abstractmethod
  async def get_user_by_email(self, email: str) -> user_schema.UserOut | None:
    pass
