import typing
from datetime import datetime

from pydantic import (BaseModel,
                      validator)


class RatingReview(BaseModel):
    user_id: str
    rating: int


class RatingReviewDelete(BaseModel):
    user_id: str


class ReviewUgcModelResponse(BaseModel):
    id: str
    film_id: str
    user_id: str
    liked_films_id: str
    text: str
    ratings: typing.List[RatingReview]
    avg_rating_review: float
    created: datetime


class ReviewUgcModel(BaseModel):
    film_id: str
    user_id: str
    text: str
    ratings: typing.List[RatingReview]
    avg_rating_review: float
    created: typing.Union[datetime, None]

    @validator('created', pre=True, always=True)
    def set_created(cls, v):
        return v or datetime.now()


class ReviewUgcModelPost(BaseModel):
    film_id: str
    user_id: str
    text: str
    created: typing.Union[datetime, None]
    liked_films_id: typing.Union[str, None]

    @validator('created', pre=True, always=True)
    def set_created(cls, v):
        return v or datetime.now()
