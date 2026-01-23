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
