from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class BookMarkUgcModel(BaseModel):
    film_id: UUID
    user_id: UUID
    created: datetime | None

    @validator('created', pre=True, always=True)
    def set_created(cls, v):
        return v or datetime.now()


class BookMarkUgcModelResponse(BaseModel):
    id: str
    film_id: UUID
    user_id: UUID
    created: datetime
