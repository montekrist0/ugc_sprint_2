import logging
import os
import sys

from pydantic import (BaseSettings,
                      Field)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    mongo_host: str = Field(default='localhost')
    mongo_port: int = Field(default='27017')
    mongo_db: str = Field(default='ugc2_films')
    mongo_collection_like: str = 'liked_films'
    mongo_collection_bookmarks: str = 'bookmarks_films'
    mongo_collection_reviewed: str = 'reviewed_films'
    sentry_dsn: str = "https://df496bbaed8a404fba24854a4b782d70@o4505008417144832.ingest.sentry.io/4505008421535744"
    traces_sample_rate: float = 1.0

    default_page_size: int = Field(default=50)
    default_page_number: int = Field(default=0)


settings = Settings()

log_format = '{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger(__name__)
