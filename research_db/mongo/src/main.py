import datetime
from abc import ABC, abstractmethod

import pymongo.database
from pymongo import MongoClient
from pymongo.results import InsertOneResult, InsertManyResult
from pymongo.errors import PyMongoError
from pymongo.database import Database, Collection

connection_string = "mongodb://root:example@localhost:27017/"


class DBManager(ABC):

    @abstractmethod
    def create_db(self, db_name: str):
        pass

    @abstractmethod
    def create_collection(self, *params):
        pass

    @abstractmethod
    def insert_one(self, collection_name, db_name, doc):
        pass

    @abstractmethod
    def insert_many(self, collection_name, db_name):
        pass


class MongoDBManager(DBManager):

    def __init__(self, con_string: str) -> None:
        self.client = MongoClient(con_string)

    def create_db(self, db_name: str) -> None | Database:
        return self.client[db_name]

    def create_collection(self, collection_name: str, db_name: str) -> None | Collection:
        return self.client[db_name][collection_name]

    def insert_one(self, collection_name: str, db_name: str, doc: dict) -> None | InsertOneResult:
        try:
            result = self.client[db_name][collection_name].insert_one(doc)
            return result

        except PyMongoError:
            return None

    def insert_many(self, collection_name, db_name):
        pass


# client = MongoClient()

# db = client.test_database
# collection = db.test_collection

# post = {
#     "author": "Mike",
#     "text": "My first blog post!",
#     "tags": ["mongodb", "python", "pymongo"],
#     "date": datetime.datetime.utcnow(),
# }

# posts = db.posts
# post_id = posts.insert_one(post).inserted_id
