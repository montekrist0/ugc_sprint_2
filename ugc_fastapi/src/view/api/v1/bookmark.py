from uuid import UUID

from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Response,
                     status)

from view.models.bookmark import (BookMarkUgcModelResponse,
                                  BookMarkUgcModel)
from view.models.pagination import PaginataionParameters
from view.services.pagination import get_pagination_parameters

router = APIRouter()


@router.get('users/{user_id}',
            response_model=list[BookMarkUgcModelResponse],
            summary='Список закладок с фильмами для юзера')
async def get_bookmarks_films(user_id: UUID,
                              pagination_parameters: PaginataionParameters = Depends(get_pagination_parameters)):
    bookmarks = ...
    if bookmarks:
        return Response(content=bookmarks, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bookmarks not found')


@router.post('',
             response_model=BookMarkUgcModelResponse,
             summary='Добавление закладки с фильмом для юзера')
async def add_bookmarks_films(bookmark_data: BookMarkUgcModel):
    bookmark = ...
    if bookmark:
        return Response(content=bookmark, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bookmark not created')


@router.delete('/{bookmark_id}', summary='Добавление закладки с фильмом у юзера')
async def remove_like_film(bookmark_id: str):
    try:
        # delete bookmark
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    # TODO возможно нужно создать собственный класс exception
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bookmark not deleted')
