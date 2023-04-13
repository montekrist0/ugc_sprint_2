from pydantic import (BaseModel,
                      Field)

from core.configs import settings


class PaginationParameters(BaseModel):
    page_size: int = Field(default=settings.default_page_size)
    page_number: int = Field(default=settings.default_page_number)

