from functools import lru_cache

from services.base import BaseService
from db.clients.mongo import get_mongo_client
from core.configs import settings


class BookMarksService(BaseService):
    pass


@lru_cache(maxsize=None)
def get_bookmarks_service():
    client = get_mongo_client()
    db = client[settings.mongo_db]
    collection = db[settings.mongo_collection_bookmarks]
    return BookMarksService(collection)
