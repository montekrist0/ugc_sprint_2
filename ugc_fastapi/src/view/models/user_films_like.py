from pydantic import BaseModel, Field


class LikeUgcModel(BaseModel):
    film_id: str
    user_id: str
    rating: int = Field(ge=0, le=10)


class LikeUgcModelResponse(BaseModel):
    id: str
    film_id: str
    user_id: str
    rating: int = Field(ge=0, le=10)


class LikeUgcModelPatch(BaseModel):
    rating: int = Field(ge=0, le=10)
