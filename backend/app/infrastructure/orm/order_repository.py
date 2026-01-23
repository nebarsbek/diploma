from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.domain.abc_repositories.order_repository import OrderRepository
from app.infrastructure.orm.models import OrderModel, OrderItemModel
from app.domain.models.order import Order
from app.domain.models.orderItem import OrderItem

class SqlOrderRepository(OrderRepository):

    def __init__(self, db):
        self.db = db

    async def save(self, order):
        if order.id:
            stmt = select(OrderModel).where(OrderModel.id == order.id)
            result = await self.db.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                model.status = order.status
                await self.db.commit()
            return order.id

        model = OrderModel(user_id=order.user_id, status=order.status, delivery_address=order.delivery_address)
        self.db.add(model)
        await self.db.flush()

        for item in order.items:
            self.db.add(OrderItemModel(
                order_id=model.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price 
            ))

        await self.db.commit()
        order.id = model.id
        return model.id

    async def get_by_user_id(self, user_id: int):
        stmt = select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.user_id == user_id)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def get_by_id(self, order_id: int):
        stmt = select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.id == order_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_all(self):
        stmt = select(OrderModel).options(selectinload(OrderModel.items)).order_by(OrderModel.id.desc())
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model):
        order = Order(user_id=model.user_id, id=model.id, status=model.status, delivery_address=model.delivery_address)
        for item in model.items:
            # Предполагаем, что в модели OrderItemModel есть поле price
            order.add_item(OrderItem(product_id=item.product_id, price=item.price, quantity=item.quantity))
        return order
