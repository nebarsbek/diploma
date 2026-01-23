from typing import List
from app.domain.models.pizza import Pizza
from app.domain.abc_repositories.pizza_repository import IPizzaRepository
from app.application.pizzas.dto import CreatePizzaIn

class GetPizzasUseCase:
    def __init__(self, repository: IPizzaRepository):
        self.repository = repository

    async def execute(self) -> List[Pizza]:
        return await self.repository.get_all()

class CreatePizzaUseCase:
    def __init__(self, repository: IPizzaRepository):
        self.repository = repository

    async def execute(self, data: CreatePizzaIn) -> Pizza:
        pizza = Pizza(
            id=None,
            name=data.name,
            price=data.price,
            description=data.description,
            category=data.category,
            image_url=data.image_url
        )
        return await self.repository.add(pizza)

class SearchPizzasUseCase:
    def __init__(self, repository: IPizzaRepository):
        self.repository = repository

    async def execute(self, query: str) -> List[Pizza]:
        return await self.repository.search(query)
