import orjson  # type: ignore
from functools import lru_cache

from services.base import BaseService
from db.clients.mongo import get_mongo_client
from core.configs import settings
from services.like import LikeService


class ReviewService(BaseService):
    @staticmethod
    async def get_user_films_like_id(film_id: str, user_id: str, like_service: LikeService):
        filter_ = {'film_id': film_id, 'user_id': user_id}
        user_films_like_doc = await like_service.find(filter_, 0, 1)
        user_films_like_doc = orjson.loads(user_films_like_doc)
        if user_films_like_doc:
            return user_films_like_doc[0]['id']
        else:
            return None

    async def is_review(self, film_id: str, user_id: str):
        filter_ = {'film_id': film_id, 'user_id': user_id}
        review = await self.find(filter_, 0, 1)
        review = orjson.loads(review)
        if review:
            return True
        return False

    async def add_rating_review(self, review: dict, rating_review: dict):
        if 'ratings' in review:
            if review['ratings'] is not None:
                ratings: list = review['ratings']
                replace = await self.replace_rating(ratings, rating_review)
                if replace:
                    review['ratings'] = replace
                else:
                    review['ratings'].append(rating_review)
        else:
            review['ratings'] = [rating_review]
        result = await self.patch_one(review['id'], review)
        return result

    @staticmethod
    async def replace_rating(ratings: list, rating_review: dict):
        for index_, rating in enumerate(ratings):
            if rating['user_id'] == rating_review['user_id']:
                ratings[index_] = rating_review
                return ratings
        return False

    async def delete_rating_review(self, review: dict, rating_review_user_id: str):
        ratings: list = review['ratings']
        rating_before_del = await self.del_rating(ratings, rating_review_user_id)
        review['ratings'] = rating_before_del
        result = await self.patch_one(review['id'], review)
        return result

    @staticmethod
    async def del_rating(ratings: list, rating_review_user_id: str):
        for index_, rating in enumerate(ratings):
            if rating['user_id'] == rating_review_user_id:
                del ratings[index_]
        return ratings


@lru_cache
def get_review_service():
    client = get_mongo_client()
    db = client[settings.mongo_db]
    collection = db[settings.mongo_collection_reviewed]
    return ReviewService(collection)
