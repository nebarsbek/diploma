from abc import ABC, abstractmethod

class OrderRepository(ABC):

    @abstractmethod
    async def save(self, order): ...

    @abstractmethod
    async def get_by_user_id(self, user_id: int): ...

    @abstractmethod
    async def get_by_id(self, order_id: int): ...

    @abstractmethod
    async def get_all(self): ...
