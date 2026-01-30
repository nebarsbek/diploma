import asyncio
import logging
from decimal import Decimal

from app.infrastructure.database import async_session_maker
from app.infrastructure.orm.models import PizzaORM, UserORM, OrderModel, OrderItemModel
from app.infrastructure.security import get_password_hash
from sqlalchemy import select, delete

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    async with async_session_maker() as session:
        # 0. Очищаем базу данных (удаляем старые данные)
        logger.info("Clearing database...")
        await session.execute(delete(OrderItemModel))
        await session.execute(delete(OrderModel))
        await session.execute(delete(PizzaORM))
        await session.execute(delete(UserORM))
        await session.commit()

        # 1. Создаем Админа
        admin_email = "admin@example.com"
        logger.info("Creating admin user...")
        admin_user = UserORM(
            email=admin_email,
            hashed_password=get_password_hash("admin"),
            role="admin",
            is_verified=True,
            is_active=True
        )
        session.add(admin_user)

        # 2. Создаем продукты (Пицца, Напитки, Десерты)
        products = [
            # Пиццы
            {"name": "Margherita", "price": "10.00", "description": "Classic tomato and mozzarella", "category": "pizza", "image_url": "https://kristineskitchenblog.com/wp-content/uploads/2024/07/margherita-pizza-22-2.jpg"},
            {"name": "Pepperoni", "price": "12.00", "description": "Spicy pepperoni slices", "category": "pizza", "image_url": "https://arecipeforfun.com/wp-content/uploads/2025/03/Edits-Turkey-Pepperoni-Pizza-Recipe-14-500x500.jpg"},
            {"name": "Hawaiian", "price": "11.50", "description": "Ham and pineapple", "category": "pizza", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWVFqf-DxD3Bfz0eo1LeuSO4njZRYObGyMnw&s"},
            {"name": "Four Cheese", "price": "13.00", "description": "Mozzarella, Cheddar, Parmesan, Blue Cheese", "category": "pizza", "image_url": "https://italianstreetkitchen.com/au/wp-content/uploads/2024/02/pizza-_0008_four_cheese_pizza_lunch.jpg"},
            {"name": "Meat Lovers", "price": "14.00", "description": "Pepperoni, ham, sausage, bacon", "category": "pizza", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmPR1_zMo2os323KG1lKiAYD3TAh18WcGYjg&s"},
            {"name": "Veggie", "price": "11.00", "description": "Peppers, onions, mushrooms, olives", "category": "pizza", "image_url": "https://placehold.co/400?text=Veggie"},
            {"name": "BBQ Chicken", "price": "13.50", "description": "Chicken, BBQ sauce, onions", "category": "pizza", "image_url": "https://placehold.co/400?text=BBQ+Chicken"},
            {"name": "Mushroom", "price": "11.00", "description": "Fresh mushrooms and herbs", "category": "pizza", "image_url": "https://placehold.co/400?text=Mushroom"},
            {"name": "Spicy Italian", "price": "12.50", "description": "Salami and chili peppers", "category": "pizza", "image_url": "https://placehold.co/400?text=Spicy+Italian"},
            {"name": "Supreme", "price": "15.00", "description": "Everything on it", "category": "pizza", "image_url": "https://placehold.co/400?text=Supreme"},

            # Напитки
            {"name": "Cola", "price": "2.50", "description": "Refreshing cola", "category": "drinks", "image_url": "https://placehold.co/400?text=Cola"},
            {"name": "Diet Cola", "price": "2.50", "description": "Sugar-free cola", "category": "drinks", "image_url": "https://placehold.co/400?text=Diet+Cola"},
            {"name": "Lemonade", "price": "3.00", "description": "Freshly squeezed", "category": "drinks", "image_url": "https://placehold.co/400?text=Lemonade"},
            {"name": "Orange Juice", "price": "3.50", "description": "100% Orange Juice", "category": "drinks", "image_url": "https://placehold.co/400?text=Orange+Juice"},
            {"name": "Apple Juice", "price": "3.50", "description": "100% Apple Juice", "category": "drinks", "image_url": "https://placehold.co/400?text=Apple+Juice"},
            {"name": "Water (Still)", "price": "1.50", "description": "Pure spring water", "category": "drinks", "image_url": "https://placehold.co/400?text=Water"},
            {"name": "Water (Sparkling)", "price": "1.50", "description": "Sparkling water", "category": "drinks", "image_url": "https://placehold.co/400?text=Sparkling+Water"},
            {"name": "Iced Tea", "price": "2.80", "description": "Peach flavored iced tea", "category": "drinks", "image_url": "https://placehold.co/400?text=Iced+Tea"},
            {"name": "Coffee", "price": "2.00", "description": "Hot brewed coffee", "category": "drinks", "image_url": "https://placehold.co/400?text=Coffee"},
            {"name": "Beer", "price": "4.00", "description": "Lager beer", "category": "drinks", "image_url": "https://placehold.co/400?text=Beer"},

            # Десерты
            {"name": "Cheesecake", "price": "5.00", "description": "New York style cheesecake", "category": "desserts", "image_url": "https://placehold.co/400?text=Cheesecake"},
            {"name": "Tiramisu", "price": "5.50", "description": "Italian coffee dessert", "category": "desserts", "image_url": "https://placehold.co/400?text=Tiramisu"},
            {"name": "Chocolate Cake", "price": "4.50", "description": "Rich chocolate cake", "category": "desserts", "image_url": "https://placehold.co/400?text=Chocolate+Cake"},
            {"name": "Brownie", "price": "3.50", "description": "Warm chocolate brownie", "category": "desserts", "image_url": "https://placehold.co/400?text=Brownie"},
            {"name": "Ice Cream (Vanilla)", "price": "3.00", "description": "Scoop of vanilla", "category": "desserts", "image_url": "https://placehold.co/400?text=Vanilla+Ice+Cream"},
            {"name": "Ice Cream (Chocolate)", "price": "3.00", "description": "Scoop of chocolate", "category": "desserts", "image_url": "https://placehold.co/400?text=Chocolate+Ice+Cream"},
            {"name": "Fruit Salad", "price": "4.00", "description": "Fresh seasonal fruits", "category": "desserts", "image_url": "https://placehold.co/400?text=Fruit+Salad"},
            {"name": "Panna Cotta", "price": "5.00", "description": "Creamy Italian dessert", "category": "desserts", "image_url": "https://placehold.co/400?text=Panna+Cotta"},
            {"name": "Muffin", "price": "2.50", "description": "Blueberry muffin", "category": "desserts", "image_url": "https://placehold.co/400?text=Muffin"},
            {"name": "Cookie", "price": "1.50", "description": "Chocolate chip cookie", "category": "desserts", "image_url": "https://placehold.co/400?text=Cookie"},
        ]

        for p_data in products:
            logger.info(f"Adding product: {p_data['name']}")
            new_product = PizzaORM(
                name=p_data["name"],
                price=Decimal(p_data["price"]),
                description=p_data["description"],
                category=p_data["category"],
                image_url=p_data["image_url"]
            )
            session.add(new_product)

        await session.commit()
        logger.info("Database initialization completed.")

if __name__ == "__main__":
    asyncio.run(init_db())
