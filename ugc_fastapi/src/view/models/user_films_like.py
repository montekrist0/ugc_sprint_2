from uuid import UUID

from pydantic import BaseModel, Field


class LikeUgcModel(BaseModel):
    film_id: UUID
    user_id: UUID
    rating: int = Field(ge=0, le=10)


class LikeUgcModelResponse(BaseModel):
    id: str
    film_id: UUID
    user_id: UUID
    rating: int = Field(ge=0, le=10)
