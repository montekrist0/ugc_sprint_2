import random
import time

import pandas as pd
import settings
from data_loader import film_ids, user_ids
from data_generator import DataGenerator
from pymongo.database import Collection
from pymongo.errors import CollectionInvalid

from research_db.mongo.src.db_manager import MongoDBManager


def test_get_avg_rating_of_films(collection: Collection, count: int = 100):
    """
    Тестирование скорости чтения средней пользовательской оценки фильма

    :param collection: коллекция в MongoDB
    :param count: количество различных film_id для выборки из коллекции
    :return:
    """
    all_time = 0
    results = []

    for _ in range(count):
        film_id = random.choice(film_ids)
        start_time = time.monotonic()

        collection.aggregate(
            [{"$match": {"film_id": film_id}}, {"$group": {"_id": None, "avg_value": {"$avg": "$rating"}}}]
        )

        avg_rating_time_getting_ms = round((time.monotonic() - start_time) * 1000, 2)
        all_time += avg_rating_time_getting_ms

        results.append(avg_rating_time_getting_ms)

    avg_time = round(all_time / count, 2)
    print(f"Average time of getting avg rating for films - {avg_time} ms")

    return results


def test_get_user_liked_films(collection: Collection, count: int = 100):
    """
    Тестирование скорости получение списка фильмов, понравившихся пользователю

    :param collection: коллекция в MongoDB
    :param count: количество различных user_id для выборки из коллекции
    :return:
    """
    all_time = 0
    like_rating = 9
    results = []

    for _ in range(count):
        user_id = random.choice(user_ids)
        start_time = time.monotonic()

        collection.find({"user_id": user_id, "rating": {"$gte": like_rating}})

        liked_films_time_getting_ms = round((time.monotonic() - start_time) * 1000, 2)
        all_time += liked_films_time_getting_ms

        results.append(liked_films_time_getting_ms)

    avg_time = round(all_time / count, 2)
    print(f"Average time of getting user liked films - {avg_time} ms")

    return results


def test_write_doc_time(collection: Collection, count: int = 100):
    """
    Тестирование скорости записи документа в коллекцию

    :param collection: коллекция в MongoDB
    :param count: количество различных user_id для выборки из коллекции
    :return:
    """
    all_time = 0
    results = []
    dg = DataGenerator()

    for _ in range(count):
        doc = dg.generate_like_doc()
        start_time = time.monotonic()

        collection.insert_one(doc)

        insert_time_ms = round((time.monotonic() - start_time) * 1000, 2)
        all_time += insert_time_ms

        results.append(insert_time_ms)

    avg_time = round(all_time / count, 2)
    print(f"Average insertion new document in collection - {avg_time} ms")

    return results


def main():
    mongodb_manager = MongoDBManager(settings.CONNECTION_STRING, settings.DB_NAME)

    try:
        like_collection = mongodb_manager.create_collection(settings.Collections.likes)
    except CollectionInvalid:
        like_collection = mongodb_manager.db.get_collection(settings.Collections.likes)

    res_1 = test_get_avg_rating_of_films(like_collection)
    res_2 = test_get_user_liked_films(like_collection)
    res_3 = test_write_doc_time(like_collection)

    pd.DataFrame(
        {
            "avg_rating_time, ms": res_1,
            "liked_films, ms": res_2,
            "doc insertion time, ms": res_3,
        }
    ).to_csv(settings.RESULTS_FILENAME)

    print(f"Tests results are saved in file '{settings.RESULTS_FILENAME}'")


if __name__ == "__main__":
    main()
