from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class RatingReview(BaseModel):
    user_id: str
    rating: int


class ReviewUgcModelResponse(BaseModel):
    id: str
    film_id: UUID
    user_id: UUID
    user_films_like_id: str
    text: str
    ratings: list[RatingReview]
    avg_rating_review: float
    created: datetime


class ReviewUgcModel(BaseModel):
    film_id: UUID
    user_id: UUID
    text: str
    # ratings: list[RatingReview]
    # avg_rating_review: float
    created: datetime | None

    @validator('created', pre=True, always=True)
    def set_created(cls, v):
        return v or datetime.now()
