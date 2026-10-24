import uuid
from datetime import UTC, datetime

from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.tortoise.business import Business


class Product(Model):
  id = fields.UUIDField(pk=True, default=uuid.uuid4, index=True)
  name = fields.CharField(max_length=255, null=False, index=True)
  category = fields.CharField(max_length=255, null=False, index=True)
  original_price = fields.DecimalField(decimal_places=2, max_digits=10, null=False)
  new_price = fields.DecimalField(decimal_places=2, max_digits=10)
  percentage_discount = fields.DecimalField(decimal_places=2, max_digits=10)
  offer_expiration_date = fields.DateField(default=datetime.now(UTC))
  product_image = fields.CharField(max_length=255, null=False, default="default.png")
  created_at = fields.DateTimeField(default=datetime.now(UTC))
  updated_at = fields.DateTimeField(default=datetime.now(UTC))
  business = fields.ForeignKeyField(
    Business, related_name="products", source_field="business_id"
  )


product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydanticIn = pydantic_model_creator(
  Product,
  name="ProductIn",
  exclude_readonly=True,
  exclude=("percentage_discount", "created_at", "updated_at"),
)
