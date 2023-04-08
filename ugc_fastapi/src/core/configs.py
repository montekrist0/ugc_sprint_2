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
    mongo_host: str = Field(env="MONGO_HOST")
    mongo_port: int = Field(env='MONGO_PORT')
    mongo_collection_like: str = 'likedFilms'
    mongo_collection_marker: str = 'markedFilms'
    mongo_collection_reviewed: str = 'reviewedFilms'
