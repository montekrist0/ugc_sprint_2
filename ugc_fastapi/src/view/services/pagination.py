from fastapi import Query

from view.models.pagination import PaginataionParameters


async def get_pagination_parameters(
        page_size: int = Query(
            default=50, alias="page[size]", title="Размер страницы", ge=1
        ),
        page_number: int = Query(
            default=0, alias="page[number]", title="Номер страницы", ge=0
        ),
):
    return PaginataionParameters(page_size=page_size, page_number=page_number)
