from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Pizza:
    id: int | None
    name: str
    price: Decimal
    description: str
    category: str
    image_url: str | None = None
