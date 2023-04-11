import os
import logging
from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path_log_file = os.path.join(BASE_DIR, 'log/logfile.json')


class Settings(BaseSettings):
    mongo_host: str = Field(env="MONGO_HOST", default='localhost')
    mongo_port: int = Field(env='MONGO_PORT', default='27017')
    mongo_db: str = Field(env='MONGO_DB', default='ugc2_films')
    mongo_collection_like: str = 'liked_films'
    mongo_collection_bookmarks: str = 'bookmarks_films'
    mongo_collection_reviewed: str = 'reviewed_films'


settings = Settings()


logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}')
file_handler = logging.FileHandler('log/logfile.json')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel('INFO')
