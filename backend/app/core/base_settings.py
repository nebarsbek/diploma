from loguru import logger
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict

from app.core.consts import env_file_path, env_file_encoding


class BaseSettings(_BaseSettings):
    logger.info(
        "Initializing BaseSettings with env file: %s",
        env_file_path,
    )
    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding=env_file_encoding,
        extra="ignore",
    )
