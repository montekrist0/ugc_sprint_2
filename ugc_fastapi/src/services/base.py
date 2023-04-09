from abc import ABC
from bson.objectid import ObjectId

from motor.motor_asyncio import AsyncIOMotorCollection

import orjson


class BaseService(ABC):

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def insert_one(self, data: dict):
        result = await self.collection.insert_one(data)
        inserted_id = result.inserted_id
        inserted_doc = await self.collection.find_one({"_id": inserted_id})
        inserted_doc = await self._transform_dict(inserted_doc)
        return inserted_doc

    async def find(self, filter_: dict, page_number: int, page_size: int):
        skip = await self._create_skip(page_number, page_size)
        cursor = self.collection.find(filter_).skip(skip).limit(page_size)
        docs = await cursor.to_list(length=None)
        docs = await self._transform_list_dict(docs)
        return docs

    async def find_one(self, id_: str):
        doc = await self.collection.find_one({"_id": ObjectId(id_)})
        if doc:
            doc = await self._transform_dict(doc)
        return doc

    async def delete_one(self, id_: str):
        filter_ = {'_id': ObjectId(id_)}
        result = await self.collection.delete_one(filter_)
        return result.deleted_count

    async def patch_one(self, id_: str, data: dict):
        await self.collection.update_one({"_id": ObjectId(id_)}, {'$set': data})
        patch_doc = await self.collection.find_one({"_id": ObjectId(id_)})
        patch_doc = await self._transform_dict(patch_doc)
        return patch_doc

    @staticmethod
    async def _obj_to_json(my_list_dist):
        return orjson.dumps(my_list_dist)

    async def _transform_list_dict(self, my_list_dict: list[dict]):
        for my_dict in my_list_dict:
            my_dict['id'] = str(my_dict.pop('_id'))
        return await self._obj_to_json(my_list_dict)

    async def _transform_dict(self, my_dict: dict):
        my_dict['id'] = str(my_dict.pop('_id'))
        return await self._obj_to_json(my_dict)

    @staticmethod
    async def _create_skip(page_number: int, page_size: int):
        skip = page_size * page_number
        return skip
