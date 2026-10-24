import uuid
from datetime import UTC, datetime

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.sqlalchemy_db import Base


class User(Base):
  __tablename__ = "users"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  username = Column(String(255), nullable=False, unique=True)
  email = Column(String(255), nullable=False, unique=True)
  password = Column(String(255), nullable=False)
  is_verified = Column(Boolean, default=False)
  join_date = Column(DateTime, default=datetime.now(UTC))
  created_at = Column(DateTime, default=datetime.now(UTC))
  updated_at = Column(DateTime, default=datetime.now(UTC))


class Business(Base):
  __tablename__ = "businesses"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = Column(String(255), nullable=False, unique=True)
  city = Column(String(255), nullable=False, default="Unspecified")
  region = Column(String(255), nullable=False, default="Unspecified")
  description = Column(String(255), nullable=False, default="Unspecified")
  logo = Column(String(255), nullable=False, default="default.png")
  owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
  created_at = Column(DateTime, default=datetime.now(UTC))
  updated_at = Column(DateTime, default=datetime.now(UTC))
  owner = relationship("User", back_populates="business")


class Product(Base):
  __tablename__ = "products"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = Column(String(255), nullable=False, index=True)
  category = Column(String(255), nullable=False, index=True)
  original_price = Column(String(255), nullable=False)
  new_price = Column(String(255), nullable=False)
  percentage_discount = Column(String(255), nullable=False)
  offer_expiration_date = Column(String(255), nullable=False)
  product_image = Column(String(255), nullable=False, default="default.png")
  created_at = Column(DateTime, default=datetime.now(UTC))
  updated_at = Column(DateTime, default=datetime.now(UTC))
  business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
  business = relationship("Business", back_populates="products")
