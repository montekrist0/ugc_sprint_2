import orjson
from uuid import UUID

from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Response,
                     status)

from view.models.review import (ReviewUgcModelResponse,
                                ReviewUgcModelPost,
                                RatingReview,
                                RatingReviewDelete)

from view.models.pagination import PaginataionParameters
from view.services.pagination import get_pagination_parameters
from services.review import ReviewService, get_review_service
from services.like import LikeService, get_like_service

router = APIRouter()


@router.post('',
             response_model=ReviewUgcModelResponse,
             summary='Добавление ревью к фильму')
async def add_review_film(review_data: ReviewUgcModelPost,
                          review_service: ReviewService = Depends(get_review_service),
                          like_service: LikeService = Depends(get_like_service)):
    review_data = review_data.dict()
    review_data['film_id'] = str(review_data['film_id'])
    review_data['user_id'] = str(review_data['user_id'])
    review = await review_service.is_review(review_data['film_id'], review_data['user_id'])
    if review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review already exists')
    user_films_like_id = await review_service.get_user_films_like_id(review_data['film_id'],
                                                                     review_data['user_id'],
                                                                     like_service)
    if user_films_like_id:
        review_data['likedFilms_id'] = user_films_like_id
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user like not found')
    review = await review_service.insert_one(review_data)
    if review:
        return Response(content=review, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review not created')


@router.get('/films/{films_id}',
            response_model=list[ReviewUgcModelResponse],
            summary='Список ревью для фильма')
async def get_reviews_films(film_id: UUID,
                            pagination_parameters: PaginataionParameters = Depends(get_pagination_parameters),
                            review_service: ReviewService = Depends(get_review_service)):
    filter_ = {'film_id': str(film_id)}
    reviews = await review_service.find(filter_,
                                        pagination_parameters.page_number,
                                        pagination_parameters.page_size)
    if reviews:
        return Response(content=reviews, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='reviews not found')


@router.delete('/{review_id}', summary='Удаление ревью у фильма')
async def remove_review_film(review_id: str, review_service: ReviewService = Depends(get_review_service)):
    try:
        result = await review_service.delete_one(review_id)
        if result:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review not deleted')


@router.post('/{review_id}/rating', summary='Добавление/изменение рейтинга ревью')
async def add_rating_review(review_id: str,
                            rating_review: RatingReview,
                            review_service: ReviewService = Depends(get_review_service)):
    rating_review = rating_review.dict()
    rating_review['user_id'] = str(rating_review['user_id'])
    review = await review_service.find_one(review_id)
    if review:
        review = orjson.loads(review)
        result = await review_service.add_rating_review(review, rating_review)
        if result:
            return Response(content=result, status_code=status.HTTP_201_CREATED)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='rating for review not created')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review not found')


@router.delete('/{review_id}/rating', summary='Удаление рейтинга у ревью')
async def remove_rating_review_film(review_id: str,
                           rating_review_user_id: RatingReviewDelete,
                           review_service: ReviewService = Depends(get_review_service)):
    try:
        rating_review_user_id = rating_review_user_id.dict()
        rating_review_user_id = str(rating_review_user_id['user_id'])
        review = await review_service.find_one(review_id)
        if review:
            review = orjson.loads(review)
            result = await review_service.delete_rating_review(review, rating_review_user_id)
            if result:
                return Response(content=result, status_code=status.HTTP_200_OK)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='rating review not found')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='rating review not found')
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='rating review not deleted')
