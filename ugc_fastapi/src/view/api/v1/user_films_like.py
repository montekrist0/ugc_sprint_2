from uuid import UUID

from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Response,
                     status)

from view.models.user_films_like import (LikeUgcModelResponse,
                                         LikeUgcModel)
from view.models.pagination import PaginataionParameters
from view.services.pagination import get_pagination_parameters

router = APIRouter()


@router.get('/films/{film_id}',
            response_model=list[LikeUgcModelResponse],
            summary='Список лайков фильма')
async def get_likes_list_for_film(film_id: UUID,
                                  pagination_parameters: PaginataionParameters = Depends(get_pagination_parameters)):
    likes = ...
    if likes:
        return Response(content=likes, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='likes not found')


@router.post('',
             response_model=LikeUgcModelResponse,
             summary='Добавление лайка фильму')
async def add_like_film(like_data: LikeUgcModel):
    like = ...
    if like:
        return Response(content=like, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not created')


@router.delete('/{like_id}', summary='Удаление лайка у фильма')
async def remove_like_film(like_id: str):
    try:
        # delete like
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    # TODO возможно нужно создать собственный класс exception
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not deleted')


@router.put('',
              response_model=LikeUgcModelResponse,
              summary='Изменение рейтинга у фильма')
async def change_rating_film(like_data: LikeUgcModel):
    try:
        like = ...
        return Response(content=like, status_code=status.HTTP_200_OK)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="like not found")


@router.get('/{like_id}',
            response_model=LikeUgcModelResponse,
            summary='Получение лайка по id')
async def get_like_by_id(like_id: str):
    like = ...
    if like:
        return Response(content=like, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not found')
