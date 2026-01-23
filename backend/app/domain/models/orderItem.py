from decimal import Decimal

class OrderItem:
    def __init__(self, product_id: int, price: Decimal, quantity: int):
        self.product_id = product_id
        self.price = price
        self.quantity = quantity
