from uuid import UUID

from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Response,
                     status)

from view.models.user_films_like import (LikeUgcModelResponse,
                                         LikeUgcModel,
                                         LikeUgcModelPatch)
from view.models.pagination import PaginataionParameters
from view.services.pagination import get_pagination_parameters
from services.like import (get_like_service,
                           LikeService)

router = APIRouter()


@router.get('/films/{film_id}',
            response_model=list[LikeUgcModelResponse],
            summary='Список лайков фильма')
async def get_likes_list_for_film(film_id: UUID,
                                  pagination_parameters: PaginataionParameters = Depends(get_pagination_parameters),
                                  like_service: LikeService = Depends(get_like_service)):
    filter_ = {'film_id': str(film_id)}
    likes = await like_service.find(filter_,
                                    pagination_parameters.page_number,
                                    pagination_parameters.page_size)
    if likes:
        return Response(content=likes, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='likes not found')


@router.post('',
             response_model=LikeUgcModelResponse,
             summary='Добавление лайка фильму')
async def add_like_film(like_data: LikeUgcModel,
                        like_service: LikeService = Depends(get_like_service)):
    like_data = like_data.dict()
    like_data['film_id'] = str(like_data['film_id'])
    like_data['user_id'] = str(like_data['user_id'])
    like = await like_service.insert_one(like_data)
    if like:
        return Response(content=like, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not created')


@router.delete('/{like_id}', summary='Удаление лайка у фильма')
async def remove_like_film(like_id: str,
                           like_service: LikeService = Depends(get_like_service)):
    try:
        result = await like_service.delete_one(like_id)
        if result:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not deleted')
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not deleted')


@router.patch('/{like_id}',
              response_model=LikeUgcModelResponse,
              summary='Изменение рейтинга у фильма')
async def change_rating_film(like_id: str,
                             like_data: LikeUgcModelPatch,
                             like_service: LikeService = Depends(get_like_service)):
    try:
        like = await like_service.patch_one(like_id, like_data.dict())
        return Response(content=like, status_code=status.HTTP_200_OK)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="like rating not update")


@router.get('/{like_id}',
            response_model=LikeUgcModelResponse,
            summary='Получение лайка по id')
async def get_like_by_id(like_id: str,
                         like_service: LikeService = Depends(get_like_service)):
    like = await like_service.find_one(like_id)
    if like:
        return Response(content=like, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not found')