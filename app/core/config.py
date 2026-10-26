from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  DATABASE_USERNAME: str
  DATABASE_PASSWORD: str
  DATABASE_HOST: str
  DATABASE_PORT: str
  DATABASE_NAME: str

  MAIL_USERNAME: str
  MAIL_PASSWORD: SecretStr
  MAIL_FROM: str
  MAIL_PORT: int
  MAIL_SERVER: str
  MAIL_TLS: bool
  MAIL_SSL: bool
  USE_CREDENTIALS: bool

  SECRET_KEY: str
  ALGORITHM: str

  model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
