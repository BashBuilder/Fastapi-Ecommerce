import uuid
from datetime import UTC, datetime

from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.tortoise.user import User


class Business(Model):
  id = fields.UUIDField(pk=True, default=uuid.uuid4, index=True)
  name = fields.CharField(max_length=255, null=False, unique=True)
  city = fields.CharField(max_length=255, null=False, default="Unspecified")
  region = fields.CharField(max_length=255, null=False, default="Unspecified")
  description = fields.TextField(null=False, default="Unspecified")
  logo = fields.CharField(max_length=255, null=False, default="default.png")
  owner = fields.ForeignKeyField(User, related_name="business", source_field="owner_id")
  created_at = fields.DateTimeField(default=datetime.now(UTC))
  updated_at = fields.DateTimeField(default=datetime.now(UTC))


business_pydantic = pydantic_model_creator(Business, name="Business")
business_pydanticIn = pydanticIn = pydantic_model_creator(
  Business,
  name="BusinessIn",
  exclude_readonly=True,
  exclude=("created_at", "updated_at"),
)
