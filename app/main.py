from fastapi import FastAPI
from models.tortoise import business, product, user
from tortoise.contrib.fastapi import register_tortoise  # type: ignore

app = FastAPI()


@app.get("/")
def read_root():
  return {"Hello": "World"}


register_tortoise(
  app,
  db_url="sqlite://database.sqlite3",
  modules={"models": [user, business, product]},
  generate_schemas=True,
  add_exception_handlers=True,
)
