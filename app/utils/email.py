from datetime import UTC, datetime, timedelta

from fastapi_mail import (
  FastMail,
  MessageSchema,
  MessageType,
)
from pydantic import NameEmail

from app.core.email_config import conf
from app.schemas import user_schema
from app.schemas.email_schema import EmailSchema
from app.schemas.user_schema import TokenPayload
from app.utils.auth import generate_token


async def send_verification_email(
  email: EmailSchema,
  instance: user_schema.UserOut,
) -> None:

  token_data = {
    "id": str(instance.id),
    "username": instance.username,
    "purpose": "email_verification",
    "exp": datetime.now(UTC) + timedelta(minutes=30),
  }

  token = generate_token(TokenPayload.model_validate(token_data).model_dump())

  verification_url = f"http://localhost:8000/verify-email?token={token}"

  message = MessageSchema(
    subject="Verify your email",
    recipients=[NameEmail(name="", email=str(address)) for address in email.email],
    body=f"""

        <h1>Verify your email</h1>

        <p>Hello {instance.username},</p>

        <p>Please verify your email by clicking the link below:</p>

        <a href="{verification_url}">Verify your email</a>

        <p>This link expires in 30 minutes.</p>
        """,
    subtype=MessageType.html,
  )

  fm = FastMail(conf)

  await fm.send_message(message)
