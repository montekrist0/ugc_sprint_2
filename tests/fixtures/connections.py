import random
from datetime import datetime

import pytest
from pymongo import MongoClient

from tests.functional.settings import settings


@pytest.fixture(scope="session")
def mongo_db():
    client = MongoClient(host=settings.mongo_host, port=settings.mongo_port)
    yield client.get_database(settings.mongo_db)
    client.close()


@pytest.fixture(scope="session")
def film_ids() -> list:
    return [f"film_{i}" for i in range(100)]


@pytest.fixture(scope="session")
def user_ids() -> list:
    return [f"user_{i}" for i in range(100)]


@pytest.fixture(scope="session")
def init_like_data(mongo_db, film_ids, user_ids):
    like_collection = mongo_db.get_collection(settings.like_collection)
    review_collection = mongo_db.get_collection(settings.review_collection)
    bookmark_collection = mongo_db.get_collection(settings.bookmark_collection)

    min_likes = 1
    max_likes = 5

    for user_id in user_ids:
        film_ids_sample = random.sample(film_ids, random.randint(min_likes, max_likes))

        like_collection.insert_many(
            [{"film_id": film_id, "user_id": user_id, "rating": random.randint(0, 10)} for film_id in film_ids_sample]
        )

        review_collection.insert_many(
            [
                {
                    "film_id": film_id,
                    "user_id": user_id,
                    "user_films_like_id": "some_object_id",
                    "text": f"{random.choice(('good', 'great', 'bad', 'the best'))} movie {film_id}",
                    "ratings": [
                        {"user_id": random.choice(user_ids), "rating": random.randint(0, 10)}
                        for _ in range(random.randint(0, 5))
                    ],
                    "avg_rating_review": round(random.random(), 1),
                    "created": datetime.now(),
                }
                for film_id in film_ids_sample
            ]
        )

        bookmark_collection.insert_many(
            [
                {"user_id": user_id, "film_id": film_id, "created": datetime.now()}
                for film_id in random.sample(film_ids, random.randint(1, 10))
            ]
        )

    yield None
