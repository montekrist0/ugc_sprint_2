import random
from http import HTTPStatus

from requests import get

from tests.functional.settings import settings


def test_get_film_reviews(film_ids):
    film_id = random.choice(film_ids)
    url = f"{settings.service_url}/api/v1/reviews/films/{film_id}"

    response = get(url=url, json={})

    assert response.status_code == HTTPStatus.OK
    print(response.json())
