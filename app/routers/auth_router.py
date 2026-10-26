from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from app.core.email_config import template
from app.db.sqlalchemy_db import get_db
from app.repository.tortoise.business_repository import TBusinessRepository
from app.repository.tortoise.user_repository import TUserRepository
from app.schemas import user_schema
from app.schemas.email_schema import EmailSchema
from app.services.auth_service import AuthService
from app.utils.auth import verify_token
from app.utils.email import send_verification_email

router = APIRouter(tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_registration(
  payload: user_schema.UserCreate, db: Session = Depends(get_db)
):
  # sqlalchemy
  # user_repo = UserRepository(db)
  # business_repo = BusinessRepository(db)

  # tortoise orm
  user_repo = TUserRepository()
  business_repo = TBusinessRepository()

  # register user
  auth_service = AuthService(user_repo, business_repo)
  user_data = await auth_service.register_user(payload)

  await send_verification_email(EmailSchema(email=[user_data.email]), user_data)
  return {"status": "ok", "data": "verification email sent to email", "user": user_data}


@router.get("/verify-email", response_class=HTMLResponse)
async def email_verification(
  request: Request, token: str = Query(...), db: Session = Depends(get_db)
):
  user_repo = TUserRepository()
  # user_repo = UserRepository(db)
  token_data = await verify_token(token)
  user = await user_repo.get_user(token_data.id)

  if user and not user.is_verified:
    user.is_verified = True
    await user_repo.update_user(user.id, user_schema.UserUpdate.model_validate(user))
    return template.TemplateResponse(
      request=request, name="verification.html", context={"username": user.username}
    )
  else:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
    )
