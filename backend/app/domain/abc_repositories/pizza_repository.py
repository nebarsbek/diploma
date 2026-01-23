from abc import ABC, abstractmethod
from typing import List
from app.domain.models.pizza import Pizza

class IPizzaRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Pizza]:
        pass
    
    @abstractmethod
    async def get_by_id(self, pizza_id: int) -> Pizza | None:
        pass

    @abstractmethod
    async def add(self, pizza: Pizza) -> Pizza:
        pass

    @abstractmethod
    async def search(self, query: str) -> List[Pizza]:
        pass
