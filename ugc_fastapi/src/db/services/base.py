from abc import ABC, abstractmethod


class BaseDbManager(ABC):
    @abstractmethod
    async def get_all(self, skip: int, limit: int):
        pass

    @abstractmethod
    async def find(self, filter_: dict):
        pass
