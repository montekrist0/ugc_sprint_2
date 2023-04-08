from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator, Field
from bson.objectid import ObjectId as BsonObjectId


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class BookMarkUgcModel(BaseModel):
    film_id: UUID
    user_id: UUID
    created: datetime | None

    @validator('created', pre=True, always=True)
    def set_created(cls, v):
        return v or datetime.now()

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BookMarkUgcModelResponse(Base):
    id: PydanticObjectId | str = Field(alias='_id')
    film_id: UUID
    user_id: UUID
    created: datetime
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
