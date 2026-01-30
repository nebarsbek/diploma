from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.abc_repositories.pizza_repository import IPizzaRepository
from app.domain.models.pizza import Pizza
from app.infrastructure.orm.models import PizzaORM

class SqlPizzaRepository(IPizzaRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Pizza]:
        result = await self.db.execute(select(PizzaORM))
        orm_pizzas = result.scalars().all()
        # Маппинг из ORM модели в Доменную модель
        return [
            Pizza(
                id=p.id,
                name=p.name,
                price=p.price,
                description=p.description,
                category=p.category,
                image_url=p.image_url
            ) for p in orm_pizzas
        ]

    async def get_by_id(self, pizza_id: int) -> Pizza | None:
        result = await self.db.execute(select(PizzaORM).where(PizzaORM.id == pizza_id))
        p = result.scalars().first()
        if not p:
            return None
        return Pizza(
            id=p.id,
            name=p.name,
            price=p.price,
            description=p.description,
            category=p.category,
            image_url=p.image_url
        )

    async def add(self, pizza: Pizza) -> Pizza:
        orm_pizza = PizzaORM(
            name=pizza.name,
            price=pizza.price,
            description=pizza.description,
            category=pizza.category,
            image_url=pizza.image_url
        )
        self.db.add(orm_pizza)
        await self.db.commit()
        await self.db.refresh(orm_pizza)
        return Pizza(
            id=orm_pizza.id,
            name=orm_pizza.name,
            price=orm_pizza.price,
            description=orm_pizza.description,
            category=orm_pizza.category,
            image_url=orm_pizza.image_url
        )

    async def search(self, query: str) -> List[Pizza]:
        result = await self.db.execute(select(PizzaORM).where(PizzaORM.name.ilike(f"%{query}%")))
        orm_pizzas = result.scalars().all()
        return [
            Pizza(
                id=p.id,
                name=p.name,
                price=p.price,
                description=p.description,
                category=p.category,
                image_url=p.image_url
            ) for p in orm_pizzas
        ]

    async def update(self, pizza: Pizza) -> Pizza | None:
        stmt = select(PizzaORM).where(PizzaORM.id == pizza.id)
        result = await self.db.execute(stmt)
        orm_pizza = result.scalars().first()

        if orm_pizza:
            orm_pizza.name = pizza.name
            orm_pizza.price = pizza.price
            orm_pizza.description = pizza.description
            orm_pizza.category = pizza.category
            orm_pizza.image_url = pizza.image_url
            
            await self.db.commit()
            await self.db.refresh(orm_pizza)
            
            # Возвращаем обновленный объект (можно мапить заново, но поля те же)
            return pizza
        return None

    async def delete(self, pizza_id: int) -> bool:
        stmt = select(PizzaORM).where(PizzaORM.id == pizza_id)
        result = await self.db.execute(stmt)
        orm_pizza = result.scalars().first()
        if orm_pizza:
            await self.db.delete(orm_pizza)
            await self.db.commit()
            return True
        return False
