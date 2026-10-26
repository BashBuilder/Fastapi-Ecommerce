from typing import Any

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash

from app.core.config import settings
from app.repository.tortoise.user_repository import TUserRepository
from app.schemas import user_schema

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
  return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
  return password_hash.verify(plain_password, hashed_password)


def generate_token(payload: dict[str, Any]) -> str:
  return jwt.encode(
    payload,
    settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
  )


def verify_token(token: str) -> user_schema.UserOut:
  try:
    decoded = jwt.decode(
      token,
      settings.SECRET_KEY,
      algorithms=[settings.ALGORITHM],
    )
    user_repo = TUserRepository()

    user = user_repo.get_user(decoded["id"])
    return user_schema.UserOut.model_validate(user)
  except jwt.ExpiredSignatureError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="The token has expired",
      headers={"WWW-Authenticate": "Bearer"},
    )
  except jwt.InvalidTokenError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="The token is invalid",
      headers={"WWW-Authenticate": "Bearer"},
    )
