from functools import lru_cache

from services.base import BaseService
from db.services.mongo import MongoDbManager
from db.clients.mongo import get_mongo_client
from core.configs import settings

import orjson
from view.models.bookmark import BookMarkUgcModelResponse

class BookMarksService(BaseService):
    def __init__(self, db_manager: MongoDbManager):
        self.db_manager = db_manager

    async def get_all(self, page_number: int, page_size: int):
        bookmarks = await self.db_manager.get_all(0, 10)
        # for _ in bookmarks:
        #     _['_id'] = str(_['_id'])
        return bookmarks


@lru_cache
def get_bookmarks_service():
    client = get_mongo_client()
    db = client[settings.mongo_db]
    collection = db[settings.mongo_collection_bookmarks]
    db_manager = MongoDbManager(collection)
    return BookMarksService(db_manager)
