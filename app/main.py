from fastapi import FastAPI

from app.db.tortoise_db import init_db
from app.routers.auth_router import router as auth_router
from app.utils.email import *

app = FastAPI()


@app.get("/")
def read_root():
  return {"Hello": "World"}


init_db(app)

app.include_router(auth_router)
