import typing

import orjson  # type: ignore
from fastapi import APIRouter, Depends, HTTPException, Response, status

from core.configs import logger
from services.like import (LikeService,
                           get_like_service)
from services.review import (ReviewService,
                             get_review_service)
from view.models.pagination import PaginationParameters
from view.models.review import (RatingReview,
                                RatingReviewDelete,
                                ReviewUgcModelPost,
                                ReviewUgcModelResponse)
from view.services.pagination import get_pagination_parameters

router = APIRouter()


@router.post('',
             response_model=ReviewUgcModelResponse,
             summary='Добавление ревью к фильму')
async def add_review_film(review_data: ReviewUgcModelPost,
                          review_service: ReviewService = Depends(get_review_service),
                          like_service: LikeService = Depends(get_like_service)):

    review = await review_service.is_review(review_data.film_id, review_data.user_id)
    if review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review already exists')

    user_films_like_id = await review_service.get_user_films_like_id(review_data.film_id,
                                                                     review_data.user_id,
                                                                     like_service)
    if user_films_like_id:
        review_data.liked_films_id = user_films_like_id
    else:
        logger.info(f"User {review_data.user_id} like not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user like not found')

    review = await review_service.insert_one(review_data.dict())

    if review:
        logger.info(f"User {review_data.user_id} review created")
        return Response(content=review, status_code=status.HTTP_201_CREATED)

    logger.info(f"User {review_data.user_id} review not created")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review not created')


@router.get('/films/{film_id}',
            response_model=typing.List[ReviewUgcModelResponse],
            summary='Список ревью для фильма')
async def get_reviews_films(film_id: str,
                            pagination_parameters: PaginationParameters = Depends(get_pagination_parameters),
                            review_service: ReviewService = Depends(get_review_service)):
    filter_ = {'film_id': film_id}
    reviews = await review_service.find(filter_,
                                        pagination_parameters.page_number,
                                        pagination_parameters.page_size)

    if reviews:
        logger.info(f"Reviews for film {film_id}")
        return Response(content=reviews, status_code=status.HTTP_200_OK)

    logger.info(f"Reviews for film {film_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='reviews not found')


@router.delete('/{review_id}', summary='Удаление ревью у фильма')
async def remove_review_film(review_id: str, review_service: ReviewService = Depends(get_review_service)):
    try:
        result = await review_service.delete_one(review_id)
        if result:
            logger.info(f"Review {review_id} deleted")
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception:
        logger.info(f"Review {review_id} not deleted")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review not deleted')


@router.post('/{review_id}/rating', summary='Добавление/изменение рейтинга ревью')
async def add_rating_review(review_id: str,
                            rating_review: RatingReview,
                            review_service: ReviewService = Depends(get_review_service)):

    review = await review_service.find_one(review_id)

    if review:
        review = orjson.loads(review)
        result = await review_service.add_rating_review(review, rating_review.dict())

        if result:
            logger.info(f"Rating for review {review_id} created")
            return Response(content=result, status_code=status.HTTP_201_CREATED)

        else:
            logger.info(f"Rating for review {review_id} not created")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='rating for review not created')

    logger.info(f"Review {review_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='review not found')


@router.delete('/{review_id}/rating', summary='Удаление рейтинга у ревью')
async def remove_rating_review_film(review_id: str,
                                    rating_review_user_id: RatingReviewDelete,
                                    review_service: ReviewService = Depends(get_review_service)):

    try:
        review = await review_service.find_one(review_id)

        if review:
            review = orjson.loads(review)
            result = await review_service.delete_rating_review(review, rating_review_user_id.user_id)

            if result:
                logger.info(f"Review {review_id} rating deleted")
                return Response(content=result, status_code=status.HTTP_200_OK)

            logger.info(f"Review {review_id} rating not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='rating review not found')

        else:
            logger.info(f"Review {review_id} rating not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='rating review not found')

    except Exception:
        logger.info(f"Review {review_id} rating not deleted")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='rating review not deleted')
