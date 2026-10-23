import uuid
from datetime import UTC, datetime

from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
  id = fields.UUIDField(pk=True, default=uuid.uuid4)
  username = fields.CharField(max_length=255, null=False, unique=True)
  email = fields.CharField(max_length=255, null=False, unique=True)
  password = fields.CharField(max_length=255, null=False)
  is_verified = fields.BooleanField(default=False)
  join_date = fields.DateTimeField(default=datetime.now(UTC))
  created_at = fields.DateTimeField(default=datetime.now(UTC))
  updated_at = fields.DateTimeField(default=datetime.now(UTC))


user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified",))
user_pydanticIn = pydanticIn = pydantic_model_creator(
  User, name="UserIn", exclude_readonly=True, exclude=("created_at", "updated_at")
)
user_pydaanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password",))
