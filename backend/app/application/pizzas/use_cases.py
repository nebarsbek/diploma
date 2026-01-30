from typing import List

from fastapi import HTTPException
from app.domain.models.pizza import Pizza
from app.domain.abc_repositories.pizza_repository import IPizzaRepository
from app.application.pizzas.dto import CreatePizzaIn, UpdatePizzaIn
from app.infrastructure.orm.pizza_repository import SqlPizzaRepository

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


class UpdatePizzaUseCase:
    def __init__(self, repository: SqlPizzaRepository):
        self.repository = repository

    async def execute(self, pizza_id: int, data: UpdatePizzaIn):
        pizza = await self.repository.get_by_id(pizza_id)
        if not pizza:
            raise HTTPException(status_code=404, detail="Pizza not found")
        
        if data.name is not None: pizza.name = data.name
        if data.price is not None: pizza.price = data.price
        if data.description is not None: pizza.description = data.description
        if data.category is not None: pizza.category = data.category
        if data.image_url is not None: pizza.image_url = data.image_url
            
        return await self.repository.update(pizza)

class DeletePizzaUseCase:
    def __init__(self, repository: SqlPizzaRepository):
        self.repository = repository

    async def execute(self, pizza_id: int):
        success = await self.repository.delete(pizza_id)
        if not success:
            raise HTTPException(status_code=404, detail="Pizza not found")
        return {"message": "Pizza deleted successfully"}