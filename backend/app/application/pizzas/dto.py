from decimal import Decimal
from pydantic import BaseModel

class PizzaOut(BaseModel):
    id: int
    name: str
    price: Decimal
    description: str
    category: str
    image_url: str | None = None

class CreatePizzaIn(BaseModel):
    name: str
    price: Decimal
    description: str
    category: str
    image_url: str | None = None

class UpdatePizzaIn(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    description: str | None = None
    category: str | None = None
    image_url: str | None = None