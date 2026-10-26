from fastapi import HTTPException, Request, status

from app.core.email_config import template
from app.interfaces.business_interface import IBusinessInterface
from app.interfaces.user_interface import IUserInterface
from app.schemas import business_schema, user_schema
from app.schemas.email_schema import EmailSchema
from app.utils.auth import verify_token
from app.utils.email import send_verification_email


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
    await send_verification_email(EmailSchema(email=[new_user.email]), new_user)

    return user_schema.UserOut.model_validate(new_user)

  async def verify_email(self, token: str, request: Request):
    token_data = await verify_token(token)

    user = await self.user_repo.get_user(token_data.id)

    if user and not user.is_verified:
      user.is_verified = True
      await self.user_repo.update_user(
        user.id, user_schema.UserUpdate.model_validate(user.model_dump())
      )

      return template.TemplateResponse(
        request=request, name="verification.html", context={"username": user.username}
      )

    elif user and user.is_verified:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User already verified"
      )
    else:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
      )
