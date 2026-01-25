from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.abc_repositories.user_repository import IUserRepository
from app.domain.models.user import User
from app.infrastructure.orm.models import UserORM

class SqlUserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(UserORM).where(UserORM.email == email))
        user_orm = result.scalars().first()
        if not user_orm:
            return None
        return User(
            id=user_orm.id,
            email=user_orm.email,
            password_hash=user_orm.hashed_password,
            is_active=user_orm.is_active,
            role=user_orm.role,
            is_verified=user_orm.is_verified
        )

    async def create(self, user: User) -> User:
        user_orm = UserORM(
            email=user.email,
            hashed_password=user.password_hash,
            is_active=user.is_active,
            role=user.role,
            is_verified=user.is_verified
        )
        self.db.add(user_orm)
        await self.db.flush()
        await self.db.commit()
        user.id = user_orm.id
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(UserORM).where(UserORM.id == user_id))
        user_orm = result.scalars().first()
        if not user_orm:
            return None
        return User(
            id=user_orm.id,
            email=user_orm.email,
            password_hash=user_orm.hashed_password,
            is_active=user_orm.is_active,
            role=user_orm.role,
            is_verified=user_orm.is_verified
        )

    async def count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(UserORM))
        return result.scalar()

    async def update(self, user: User) -> User:
        stmt = select(UserORM).where(UserORM.id == user.id)
        result = await self.db.execute(stmt)
        user_orm = result.scalars().first()
        if user_orm:
            user_orm.is_verified = user.is_verified
            user_orm.hashed_password = user.password_hash
            await self.db.commit()
        return user