import os
import logging
from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path_log_file = os.path.join(BASE_DIR, 'log/logfile.json')

logging.basicConfig(level=logging.INFO,
                    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s",'
                           ' "module": "%(module)s", "message": %(message)s}',
                    filename=path_log_file)


class Settings(BaseSettings):
    mongo_host: str = Field(env="MONGO_HOST", default='localhost')
    mongo_port: int = Field(env='MONGO_PORT', default='27017')
    mongo_db: str = Field(env='MONGO_DBT', default='ugc2')
    mongo_collection_like: str = 'likedFilms'
    mongo_collection_bookmarks: str = 'bookmarksFilms'
    mongo_collection_reviewed: str = 'reviewedFilms'


settings = Settings()
