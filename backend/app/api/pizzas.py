from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.infrastructure.database import get_db
from app.infrastructure.orm.pizza_repository import SqlPizzaRepository
from app.application.pizzas.use_cases import GetPizzasUseCase, CreatePizzaUseCase, SearchPizzasUseCase, UpdatePizzaUseCase, DeletePizzaUseCase
from app.application.pizzas.dto import PizzaOut, CreatePizzaIn, UpdatePizzaIn

router = APIRouter()



def get_pizzas_use_case(db=Depends(get_db)) -> GetPizzasUseCase:
    return GetPizzasUseCase(SqlPizzaRepository(db))

def get_create_pizza_use_case(db=Depends(get_db)) -> CreatePizzaUseCase:
    return CreatePizzaUseCase(SqlPizzaRepository(db))

def get_search_pizzas_use_case(db=Depends(get_db)) -> SearchPizzasUseCase:
    return SearchPizzasUseCase(SqlPizzaRepository(db))

def get_update_pizza_use_case(db=Depends(get_db)) -> UpdatePizzaUseCase:
    return UpdatePizzaUseCase(SqlPizzaRepository(db))

def get_delete_pizza_use_case(db=Depends(get_db)) -> DeletePizzaUseCase:
    return DeletePizzaUseCase(SqlPizzaRepository(db))

@router.get("/", response_model=list[PizzaOut])
async def get_pizzas(
    category: str | None = None,
    uc: GetPizzasUseCase = Depends(get_pizzas_use_case)
):
    """
    Получить список всех пицц.
    """
    products = await uc.execute()
    if category:
        return [p for p in products if p.category == category]
    return products

@router.post("/", response_model=PizzaOut)
async def create_pizza(
    data: CreatePizzaIn,
    uc: CreatePizzaUseCase = Depends(get_create_pizza_use_case)
):
    """
    Создать новую пиццу.
    """
    return await uc.execute(data)

@router.get("/search", response_model=list[PizzaOut])
async def search_pizzas(
    query: str,
    uc: SearchPizzasUseCase = Depends(get_search_pizzas_use_case)
):
    """
    Поиск пицц по названию.
    """
    return await uc.execute(query)

@router.put("/{pizza_id}", response_model=PizzaOut)
async def update_pizza(
    pizza_id: int,
    data: UpdatePizzaIn,
    uc: UpdatePizzaUseCase = Depends(get_update_pizza_use_case)
):
    """
    Обновить данные пиццы (частичное обновление).
    """
    return await uc.execute(pizza_id, data)

@router.delete("/{pizza_id}")
async def delete_pizza(
    pizza_id: int,
    uc: DeletePizzaUseCase = Depends(get_delete_pizza_use_case)
):
    """
    Удалить пиццу.
    """
    return await uc.execute(pizza_id)
