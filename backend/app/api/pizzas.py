from fastapi import APIRouter, Depends
from app.infrastructure.database import get_db
from app.infrastructure.orm.pizza_repository import SqlPizzaRepository
from app.application.pizzas.use_cases import GetPizzasUseCase, CreatePizzaUseCase, SearchPizzasUseCase
from app.application.pizzas.dto import PizzaOut, CreatePizzaIn

router = APIRouter()

def get_pizzas_use_case(db=Depends(get_db)) -> GetPizzasUseCase:
    return GetPizzasUseCase(SqlPizzaRepository(db))

def get_create_pizza_use_case(db=Depends(get_db)) -> CreatePizzaUseCase:
    return CreatePizzaUseCase(SqlPizzaRepository(db))

def get_search_pizzas_use_case(db=Depends(get_db)) -> SearchPizzasUseCase:
    return SearchPizzasUseCase(SqlPizzaRepository(db))

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
