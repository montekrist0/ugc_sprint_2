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
from services.bookmarks import get_bookmarks_service, BookMarksService

router = APIRouter()


@router.get('/users/{user_id}',
            # response_model=list[BookMarkUgcModelResponse],
            summary='Список закладок с фильмами для юзера')
async def get_bookmarks_films(user_id: UUID,
                              pagination_parameters: PaginataionParameters = Depends(get_pagination_parameters),
                              bookmarks_service: BookMarksService = Depends(get_bookmarks_service)):
    bookmarks = await bookmarks_service.get_all(pagination_parameters.page_number, pagination_parameters.page_size)
    print(bookmarks)
    if bookmarks:
        # return Response(content=bookmarks, status_code=status.HTTP_200_OK)
        print([BookMarkUgcModelResponse(**bookmark) for bookmark in bookmarks])
        return [BookMarkUgcModelResponse(**bookmark) for bookmark in bookmarks]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bookmarks not found')


@router.post('',
             # response_model=BookMarkUgcModelResponse,
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
