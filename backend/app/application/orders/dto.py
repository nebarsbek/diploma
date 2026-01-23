from decimal import Decimal
from pydantic import BaseModel

class OrderItemIn(BaseModel):
    product_id: int
    quantity: int

class CreateOrderIn(BaseModel):
    items: list[OrderItemIn]
    delivery_address: str

class CreateOrderOut(BaseModel):
    order_id: int

class OrderStatusUpdateIn(BaseModel):
    status: str

class OrderItemOut(BaseModel):
    product_id: int
    price: Decimal
    quantity: int

class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    delivery_address: str | None = None
    items: list[OrderItemOut]
    total_price: Decimal

    class Config:
        from_attributes = True
