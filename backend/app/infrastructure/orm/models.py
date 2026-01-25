from sqlalchemy import Boolean, Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

class PizzaORM(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False, default="pizza")
    image_url = Column(String, nullable=True)


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    status = Column(String, default="pending")
    delivery_address = Column(String, nullable=True)
    items = relationship("OrderItemModel", back_populates="order")

class OrderItemModel(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("OrderModel", back_populates="items")

class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="employee", nullable=False, server_default="'employee'")
    is_verified = Column(Boolean, default=False)
