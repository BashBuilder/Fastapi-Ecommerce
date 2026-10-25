from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.sqlalchemy_db import get_db
from app.repository.sqlalchemy.user_repository import UserRepository
from app.repository.tortoise.user_repository import TUserRepository
from app.schemas import user_schema
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_registration(
  payload: user_schema.UserCreate, db: Session = Depends(get_db)
):
  # sqlalchemy
  user_repo = UserRepository(db)
  auth_service = AuthService(user_repo)
  test_user = await auth_service.register_user(payload)

  # test_user = user_repo.create_user(payload)

  # tortoise orm
  t_user_repo = TUserRepository()
  auth_service2 = AuthService(t_user_repo)
  test_user2 = await auth_service2.register_user(payload)
  # test_user2 = await t_user_repo.create_user(payload)

  return {
    "status": "ok",
    "data": "verification email sent to email",
    "test_user": test_user,
    "test_user2": test_user2,
  }
