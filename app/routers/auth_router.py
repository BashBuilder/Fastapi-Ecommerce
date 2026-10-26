# from authentication import *
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from app.db.sqlalchemy_db import get_db
from app.repository.tortoise.business_repository import TBusinessRepository
from app.repository.tortoise.user_repository import TUserRepository
from app.schemas import user_schema
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_registration(
  payload: user_schema.UserCreate, db: Session = Depends(get_db)
):
  # sqlalchemy
  # user_repo = UserRepository(db)
  # business_repo = BusinessRepository(db)
  auth_service = AuthService(TUserRepository(), TBusinessRepository())
  user_data = await auth_service.register_user(payload)

  return {"status": "ok", "data": "verification email sent to email", "user": user_data}


@router.get("/verify-email", response_class=HTMLResponse)
async def email_verification(
  request: Request, token: str = Query(...), db: Session = Depends(get_db)
) -> HTMLResponse:
  auth_service = AuthService(TUserRepository(), TBusinessRepository())
  return await auth_service.verify_email(token, request)


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
  auth_service = AuthService(TUserRepository(), TBusinessRepository())
  payload = {
    "username": form_data.username,
    "password": form_data.password,
  }
  return await auth_service.login(user_schema.UserLogin.model_validate(payload))


@router.get("/me")
async def get_user(token: str = Depends(oauth2_scheme)):
  auth_service = AuthService(TUserRepository(), TBusinessRepository())

  return await auth_service.get_user(token)
