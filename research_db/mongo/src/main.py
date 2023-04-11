import random
import time
import pprint

from pymongo.database import Collection
from pymongo.errors import CollectionInvalid
from tqdm import tqdm

import settings
from research_db.mongo.src.db_manager import MongoDBManager
from data_loader import film_ids, user_ids


def test_get_avg_rating_of_films(collection: Collection, count: int = 100):
    """

    :param collection: коллекция в MongoDB
    :param count: количество различных film_id для выборки из коллекции
    :return:
    """
    all_time = 0
    for _ in range(count):

        film_id = random.choice(film_ids)
        start_time = time.monotonic()

        result = collection.aggregate([
            {"$match": {"film_id": film_id}},
            {"$group": {"_id": None, "avg_value": {"$avg": "$rating"}}}
        ])

        avg_rating_time_getting = time.monotonic() - start_time
        all_time += avg_rating_time_getting
        print(f"Get avg rating in {round(avg_rating_time_getting * 1000)} ms")

    avg_time = all_time/count
    print(f"Average time of getting avg rating for films - {round(avg_time* 1000)} ms")


def test_get_user_liked_films(collection: Collection, count: int = 200):
    """

    :param collection: коллекция в MongoDB
    :param count: количество различных user_id для выборки из коллекции
    :return:
    """
    all_time = 0
    for _ in range(count):

        user_id = random.choice(user_ids)
        start_time = time.monotonic()

        liked_films = list(collection.find({"user_id": user_id, "rating": {"$gte": 9}}))

        liked_films_time_getting = time.monotonic() - start_time
        all_time += liked_films_time_getting
        pprint.pprint(f"Get user liked films in {round(liked_films_time_getting * 1000)} ms. ")
        pprint.pprint(liked_films)

    avg_time = all_time/count
    print(f"Average time of getting user liked films - {round(avg_time* 1000)} ms")


def main():
    mongodb_manager = MongoDBManager(settings.CONNECTION_STRING, settings.DB_NAME)

    try:
        like_collection = mongodb_manager.create_collection(settings.Collections.likes)
    except CollectionInvalid:
        like_collection = mongodb_manager.db.get_collection(settings.Collections.likes)

    # test_get_avg_rating_of_films(like_collection)
    test_get_user_liked_films(like_collection)


if __name__ == "__main__":
    main()
