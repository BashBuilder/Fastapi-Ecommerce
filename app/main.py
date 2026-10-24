from fastapi import FastAPI

from app.db.tortoise_db import init_db

app = FastAPI()


@app.get("/")
def read_root():
  return {"Hello": "World"}


init_db(app)
