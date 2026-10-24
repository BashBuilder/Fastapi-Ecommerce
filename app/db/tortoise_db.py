from pathlib import Path

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise  # type: ignore[reportUnknownVariableType]

BASE_DIR = Path(__file__).resolve().parents[2]
DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_URL = f"sqlite://{DB_DIR / 'database.sqlite3'}"


def init_db(app: FastAPI) -> None:
  register_tortoise(
    app,
    db_url=DB_URL,
    modules={
      "models": [
        "app.models.tortoise.user",
        "app.models.tortoise.business",
        "app.models.tortoise.product",
      ]
    },
    generate_schemas=True,
    add_exception_handlers=True,
  )
