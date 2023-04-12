import os
from pathlib import Path

from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    mongo_host: str = Field("localhost", env="MONGO_HOST")
    mongo_port: int = Field(27017, env="MONGO_PORT")
    mongo_db: str = Field("ugc2_movies", env="MONGO_DB")
    service_url: str = Field("http://localhost:8001", env="UGC_SERVICE_URL")

    like_collection: str = Field("liked_films", env="LIKE_COL")
    bookmark_collection: str = Field("bookmarks_films", env="BOOKMARK_COL")
    review_collection: str = Field("reviewed_films", env="REVIEWS_COL")

    class Config:
        env_file = os.path.join(Path(__file__).parent.absolute(), ".env")
        env_file_encoding = "utf-8"


settings = BaseConfig()
