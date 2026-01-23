from fastapi import APIRouter, Depends
from app.infrastructure.database import get_db
from app.infrastructure.orm.order_repository import SqlOrderRepository
from app.infrastructure.orm.pizza_repository import SqlPizzaRepository
from app.application.orders.use_cases import CreateOrderUseCase, GetOrdersUseCase, UpdateOrderStatusUseCase
from app.application.orders.dto import CreateOrderIn, OrderOut, OrderStatusUpdateIn, CreateOrderOut
from app.api.dependencies import get_current_user, get_current_user_optional
from app.domain.models.user import User

router = APIRouter()

def get_create_order_use_case(db=Depends(get_db)) -> CreateOrderUseCase:
    return CreateOrderUseCase(
        SqlOrderRepository(db),
        SqlPizzaRepository(db)
    )

def get_orders_use_case(db=Depends(get_db)) -> GetOrdersUseCase:
    return GetOrdersUseCase(SqlOrderRepository(db))

def get_update_order_status_use_case(db=Depends(get_db)) -> UpdateOrderStatusUseCase:
    return UpdateOrderStatusUseCase(SqlOrderRepository(db))

@router.post("/create", response_model=CreateOrderOut)
async def create_order(
    data: CreateOrderIn, 
    uc: CreateOrderUseCase = Depends(get_create_order_use_case),
    current_user: User | None = Depends(get_current_user_optional)
):
    """
    Создать новый заказ.

    Принимает список позиций заказа (id пиццы и количество).
    Не требует обязательной авторизации.
    """
    user_id = current_user.id if current_user else None
    return {"order_id": await uc.execute(user_id=user_id, items=data.items, delivery_address=data.delivery_address)}

@router.get("/", response_model=list[OrderOut])
async def get_orders(
    uc: GetOrdersUseCase = Depends(get_orders_use_case),
    current_user: User = Depends(get_current_user)
):
    """
    Получить список заказов.
    Сотрудники и админы видят все заказы.
    """
    if current_user.role in ['admin', 'employee']:
        return await uc.execute(user_id=None)
    return await uc.execute(user_id=current_user.id) # Fallback for regular users if any

@router.patch("/{order_id}/status", response_model=OrderOut)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdateIn,
    uc: UpdateOrderStatusUseCase = Depends(get_update_order_status_use_case),
    current_user: User = Depends(get_current_user)
):
    """
    Изменить статус заказа. Только для админов.
    """
    if current_user.role != 'admin':
         raise HTTPException(status_code=403, detail="Only admin can update status")
    return await uc.execute(order_id=order_id, status=data.status)
