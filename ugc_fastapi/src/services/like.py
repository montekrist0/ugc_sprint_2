from functools import lru_cache

from services.base import BaseService
from db.clients.mongo import get_mongo_client
from core.configs import settings


class LikeService(BaseService):
    pass


@lru_cache
def get_like_service():
    client = get_mongo_client()
    db = client[settings.mongo_db]
    collection = db[settings.mongo_collection_like]
    return LikeService(collection)
