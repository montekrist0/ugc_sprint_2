from abc import ABC, abstractmethod


class BaseService(ABC):
    @abstractmethod
    async def get_all(self, page_number: int, page_size: int):
        pass
