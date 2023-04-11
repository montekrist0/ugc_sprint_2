import random
import time

from pymongo.database import Collection
from pymongo.errors import CollectionInvalid
from research_db.mongo.src.db_manager import MongoDBManager
from tqdm import tqdm

import settings


def test_get_avg_rating_of_films(collection: Collection, count: int = 100):
    pass


def main():
    mongodb_manager = MongoDBManager(settings.CONNECTION_STRING, settings.DB_NAME)

    try:
        like_collection = mongodb_manager.create_collection(settings.Collections.likes)
    except CollectionInvalid:
        like_collection = mongodb_manager.db.get_collection(settings.Collections.likes)

    test_get_avg_rating_of_films(like_collection)


if __name__ == "__main__":
    main()
