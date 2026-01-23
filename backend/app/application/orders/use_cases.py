from app.domain.models.order import Order
from app.domain.models.orderItem import OrderItem

class CreateOrderUseCase:

    def __init__(self, order_repo, pizza_repo):
        self.order_repo = order_repo
        self.pizza_repo = pizza_repo

    async def execute(self, user_id: int | None, items, delivery_address: str):
        order = Order(user_id, delivery_address=delivery_address)

        for item in items:
            product = await self.pizza_repo.get_by_id(item.product_id)
            order.add_item(
                OrderItem(
                    product_id=product.id,
                    price=product.price,
                    quantity=item.quantity
                )
            )

        return await self.order_repo.save(order)

class GetOrdersUseCase:
    def __init__(self, order_repo):
        self.order_repo = order_repo

    async def execute(self, user_id: int = None):
        if user_id is None:
            return await self.order_repo.get_all()
        return await self.order_repo.get_by_user_id(user_id)

class UpdateOrderStatusUseCase:
    def __init__(self, order_repo):
        self.order_repo = order_repo

    async def execute(self, order_id: int, status: str):
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            return None
        order.status = status
        await self.order_repo.save(order)
        return order
