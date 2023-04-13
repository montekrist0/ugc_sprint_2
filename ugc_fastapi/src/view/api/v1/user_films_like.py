import typing

from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Response,
                     status)

from core.configs import logger
from services.like import (LikeService,
                           get_like_service)
from view.models.pagination import PaginationParameters
from view.models.user_films_like import (LikeUgcModel,
                                         LikeUgcModelPatch,
                                         LikeUgcModelResponse)
from view.services.pagination import get_pagination_parameters

router = APIRouter()


@router.get('/films/{film_id}',
            response_model=typing.List[LikeUgcModelResponse],
            summary='Список лайков фильма')
async def get_likes_list_for_film(film_id: str,
                                  pagination_parameters: PaginationParameters = Depends(get_pagination_parameters),
                                  like_service: LikeService = Depends(get_like_service)):
    filter_ = {'film_id': film_id}
    likes = await like_service.find(filter_,
                                    pagination_parameters.page_number,
                                    pagination_parameters.page_size)
    if likes:
        logger.info(f"Film {film_id} likes {likes}")
        return Response(content=likes, status_code=status.HTTP_200_OK)
    else:
        logger.info(f"Film {film_id} likes not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='likes not found')


@router.post('',
             response_model=LikeUgcModelResponse,
             summary='Добавление лайка фильму')
async def add_like_film(like_data: LikeUgcModel,
                        like_service: LikeService = Depends(get_like_service)):
    like = await like_service.insert_one(like_data.dict())
    if like:
        logger.info(f"Like to film {like_data.film_id} created")
        return Response(content=like, status_code=status.HTTP_201_CREATED)
    else:
        logger.info(f"Like to film {like_data.film_id} not created")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not created')


@router.delete('/{like_id}', summary='Удаление лайка у фильма')
async def remove_like_film(like_id: str,
                           like_service: LikeService = Depends(get_like_service)):
    try:
        result = await like_service.delete_one(like_id)
        if result:
            logger.info(f"Like {like_id} deleted")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logger.info(f"Like {like_id} not deleted")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not deleted')
    except Exception:
        logger.info(f"Like {like_id} not deleted")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not deleted')


@router.patch('/{like_id}',
              response_model=LikeUgcModelResponse,
              summary='Изменение рейтинга у фильма')
async def change_rating_film(like_id: str,
                             like_data: LikeUgcModelPatch,
                             like_service: LikeService = Depends(get_like_service)):
    try:
        like = await like_service.patch_one(like_id, like_data.dict())
        logger.info(f"Like {like_id} updated")
        return Response(content=like, status_code=status.HTTP_200_OK)
    except Exception:
        logger.info(f"Like {like_id} not updated")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="like rating not update")


@router.get('/{like_id}',
            response_model=LikeUgcModelResponse,
            summary='Получение лайка по id')
async def get_like_by_id(like_id: str,
                         like_service: LikeService = Depends(get_like_service)):
    like = await like_service.find_one(like_id)
    if like:
        logger.info(f"Like {like_id} found")
        return Response(content=like, status_code=status.HTTP_200_OK)
    else:
        logger.info(f"Like {like_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='like not found')
