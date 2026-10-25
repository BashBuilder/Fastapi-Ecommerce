from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.sqlalchemy_db import get_db
from app.repository.sqlalchemy.business_repository import BusinessRepository
from app.repository.sqlalchemy.user_repository import UserRepository
from app.schemas import user_schema
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_registration(
  payload: user_schema.UserCreate, db: Session = Depends(get_db)
):
  # sqlalchemy
  user_repo = UserRepository(db)
  business_repo = BusinessRepository(db)
  auth_service = AuthService(user_repo, business_repo)
  test_user = await auth_service.register_user(payload)

  # tortoise orm
  # t_user_repo = TUserRepository()
  # t_business_repo = TBusinessRepository()
  # auth_service2 = AuthService(t_user_repo, t_business_repo)
  # test_user2 = await auth_service2.register_user(payload)

  return {
    "status": "ok",
    "data": "verification email sent to email",
    "test_user": test_user,
    # "test_user2": test_user2,
  }
