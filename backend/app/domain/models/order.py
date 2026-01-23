class Order:
    def __init__(self, user_id: int | None, id: int = None, status: str = "pending", delivery_address: str = None):
        self.id = id
        self.user_id = user_id
        self.status = status
        self.delivery_address = delivery_address
        self.items: list = []

    def add_item(self, item):
        if item.quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.items.append(item)

    @property
    def total_price(self):
        return sum(i.price * i.quantity for i in self.items)
