from pathlib import Path

from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig

from app.core.config import settings

conf = ConnectionConfig(
  MAIL_USERNAME=settings.MAIL_USERNAME,
  MAIL_PASSWORD=settings.MAIL_PASSWORD,
  MAIL_FROM=settings.MAIL_FROM,
  MAIL_PORT=settings.MAIL_PORT,
  MAIL_SERVER=settings.MAIL_SERVER,
  MAIL_STARTTLS=settings.MAIL_TLS,
  MAIL_SSL_TLS=settings.MAIL_SSL,
  USE_CREDENTIALS=settings.USE_CREDENTIALS,
)


BASE_DIR = Path(__file__).resolve().parent.parent

template = Jinja2Templates(directory=BASE_DIR / "templates")
