from functools import lru_cache

from core.configs import settings
from db.clients.mongo import get_mongo_client
from services.base import BaseService


class LikeService(BaseService):
    pass


@lru_cache(maxsize=None)
def get_like_service():
    client = get_mongo_client()
    db = client[settings.mongo_db]
    collection = db[settings.mongo_collection_like]
    return LikeService(collection)
