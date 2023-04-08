from uuid import UUID

from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Response,
                     status)

from view.models.review import (ReviewUgcModelResponse,
                                ReviewUgcModel)
from view.models.pagination import PaginataionParameters
from view.services.pagination import get_pagination_parameters

router = APIRouter()


@router.get('/films/{films_id}',
            response_model=list[ReviewUgcModelResponse],
            summary='Список закладок с фильмами для юзера')
async def get_reviews_films(films_id: UUID,
                            pagination_parameters: PaginataionParameters = Depends(get_pagination_parameters)):
    reviews = ...
    if reviews:
        return Response(content=reviews, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='reviews not found')


@router.post('',
             response_model=ReviewUgcModelResponse,
             summary='Добавление ревью к фильму')
async def add_review_film(review_data: ReviewUgcModel):
    review = ...
    if review:
        return Response(content=review, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review not created')


@router.put('',
              response_model=ReviewUgcModelResponse,
              summary='Изменение ревью')
async def change_review_film(review_data: ReviewUgcModel):
    try:
        review = ...
        return Response(content=review, status_code=status.HTTP_200_OK)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="review not found")


@router.delete('/{review_id}', summary='Удаление ревью у фильма')
async def remove_like_film(review_id: str):
    try:
        # delete like
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    # TODO возможно нужно создать собственный класс exception
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review not deleted')
