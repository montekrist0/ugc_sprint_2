from pydantic import BaseModel


class PaginataionParameters(BaseModel):
    page_size: int | None
    page_number: int | None
