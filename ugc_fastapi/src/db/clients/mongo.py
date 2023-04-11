import motor.motor_asyncio  # type: ignore
from motor.motor_asyncio import AsyncIOMotorCollection  # type: ignore

from core.configs import settings

host = settings.mongo_host
port = settings.mongo_port

client: AsyncIOMotorCollection | None = None


def create_mongo_client():
    return motor.motor_asyncio.AsyncIOMotorClient(host=host, port=port, maxPoolSize=10)


def get_mongo_client():
    return client
