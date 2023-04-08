from pydantic import BaseModel


class PaginataionParameters(BaseModel):
    page_size: str | None
    page_number: str | None
