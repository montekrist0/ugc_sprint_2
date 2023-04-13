import typing

from fastapi import APIRouter, Depends, HTTPException, Response, status

from core.configs import logger
from services.bookmarks import (BookMarksService,
                                get_bookmarks_service)
from view.models.bookmark import (BookMarkUgcModel,
                                  BookMarkUgcModelResponse)
from view.models.pagination import PaginationParameters
from view.services.pagination import get_pagination_parameters

router = APIRouter()


@router.get('/users/{user_id}',
            response_model=typing.List[BookMarkUgcModelResponse],
            summary='Список закладок с фильмами для юзера')
async def get_bookmarks_films(user_id: str,
                              pagination_parameters: PaginationParameters = Depends(get_pagination_parameters),
                              bookmarks_service: BookMarksService = Depends(get_bookmarks_service)):
    filter_ = {'user_id': user_id}
    bookmarks = await bookmarks_service.find(filter_,
                                             pagination_parameters.page_number,
                                             pagination_parameters.page_size)
    if bookmarks:
        logger.info(f"Bookmarks for user {user_id} found")
        return Response(content=bookmarks, status_code=status.HTTP_200_OK)

    logger.info(f"Bookmarks for user {user_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bookmarks not found')


@router.post('',
             response_model=BookMarkUgcModelResponse,
             summary='Добавление закладки с фильмом для юзера')
async def add_bookmarks_films(bookmark_data: BookMarkUgcModel,
                              bookmarks_service: BookMarksService = Depends(get_bookmarks_service)):
    bookmark = await bookmarks_service.insert_one(bookmark_data.dict())
    if bookmark:
        logger.info(f"Bookmark by user {bookmark_data.film_id} to film {bookmark_data.film_id} created")
        return Response(content=bookmark, status_code=status.HTTP_201_CREATED)

    logger.info(f"Bookmark by user {bookmark_data.film_id} to film {bookmark_data.film_id} not created")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bookmark not created')


@router.delete('/{bookmark_id}', summary='Удаление закладки')
async def remove_like_film(bookmark_id: str,
                           bookmarks_service: BookMarksService = Depends(get_bookmarks_service)):
    try:
        result = await bookmarks_service.delete_one(bookmark_id)
        if result:
            logger.info(f"Bookmark {bookmark_id} deleted")
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        logger.info(f"Bookmark {bookmark_id} not deleted")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bookmark not deleted')

    except Exception:
        logger.info(f"Bookmark {bookmark_id} not deleted")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bookmark not deleted')
