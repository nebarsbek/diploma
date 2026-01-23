from pydantic import EmailStr, Field

from .base_schema import BaseSchema


class UserCreate(BaseSchema):
    name: str = Field(
        ...,
        json_schema_extra={'example': 'Rubick'},
    )
    email: EmailStr = Field(
        ...,
        json_schema_extra={'example': 'rubick.aghanim@dota.com'},
    )


class UserUpdate(BaseSchema):
    id: int = Field()
    name: str = Field()
    email: EmailStr = Field()
