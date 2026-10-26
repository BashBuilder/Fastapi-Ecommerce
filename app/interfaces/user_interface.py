from abc import abstractmethod
from uuid import UUID

from app.schemas import user_schema


class IUserInterface:
  @abstractmethod
  async def create_user(self, payload: user_schema.UserCreate) -> user_schema.UserOut:
    pass

  @abstractmethod
  async def get_user(self, id: UUID | str) -> user_schema.UserOut | None:
    pass

  @abstractmethod
  async def get_user_by_email(self, email: str) -> user_schema.UserOut | None:
    pass

  @abstractmethod
  async def update_user(
    self, id: UUID | str, payload: user_schema.UserUpdate
  ) -> user_schema.UserOut:
    pass
