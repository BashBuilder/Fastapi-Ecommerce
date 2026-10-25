# from typing import Annotated

# from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# from app.db.sqlalchemy_db import Session

DATABASE_USERNAME = settings.DATABASE_USERNAME
DATABASE_PASSWORD = settings.DATABASE_PASSWORD
DATABASE_HOST = settings.DATABASE_HOST
DATABASE_PORT = settings.DATABASE_PORT
DATABASE_NAME = settings.DATABASE_NAME

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


# DbSession = Annotated[Session, Depends(get_db)]
