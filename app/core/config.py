from pydantic.env_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  DATABASE_USERNAME: str
  DATABASE_PASSWORD: str
  DATABASE_HOST: str
  DATABASE_PORT: str
  DATABASE_NAME: str

  model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
