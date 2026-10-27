from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.tortoise_db import init_db
from app.routers.auth_router import router as auth_router
from app.utils.email import *

app = FastAPI()


@app.get("/")
def read_root():
  return {"Hello": "World"}


init_db(app)

BaseDir = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=BaseDir / "static"), name="static")

app.include_router(auth_router)
