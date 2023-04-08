from db.services.base import BaseDbManager
from motor.motor_asyncio import AsyncIOMotorCollection


class MongoDbManager(BaseDbManager):
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection: AsyncIOMotorCollection = collection

    async def get_all(self, skip: int, limit: int):
        cursor = self.collection.find().skip(skip).limit(limit)
        result = await cursor.to_list(length=None)
        return result

    async def find(self, filter_: dict):
        cursor = self.collection.find(filter_)
        result = await cursor.to_list(length=None)
        return result

