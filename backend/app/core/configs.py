from loguru import logger
from pydantic import SecretStr
from sqlalchemy.engine import URL

from app.core.base_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_USER: str

    @property
    def url(self) -> URL:
        url: URL = URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )
        logger.info(f"Database URL: {url}")
        return url

    @property
    def test_url(self) -> str:
        url: str = "sqlite+aiosqlite:///:memory:"
        return url


class RedisSettings(BaseSettings):
    ...


class SQLAlchemySettings(BaseSettings):
    ALCHEMY_ECHO: bool = False
    ALCHEMY_ECHO_POOL: bool = False
    ALCHEMY_POOL_SIZE: int = 25
    ALCHEMY_MAX_OVERFLOW: int = 50
    ALCHEMY_POOL_TIMEOUT: int = 10
    ALCHEMY_POOL_RECYCLE: int = 3600


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


class Settings(BaseSettings):
    database_settings: DatabaseSettings = DatabaseSettings()  # type: ignore[call-arg]
    redis_settings: RedisSettings = RedisSettings()  # type: ignore[call-arg]
    sql_alchemy_settings: SQLAlchemySettings = SQLAlchemySettings()  # type: ignore[call-arg]
    jwt_settings: JWTSettings = JWTSettings()  # type: ignore[call-arg]


settings = Settings()
