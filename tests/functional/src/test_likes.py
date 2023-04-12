import random
from http import HTTPStatus

from requests import get

from tests.functional.settings import settings
from tests.functional.utils.helpers import valid_likes_response


def test_get_films_like(init_like_data, film_ids):
    film_id = random.choice(film_ids)
    url = f"{settings.service_url}/api/v1/likes/films/{film_id}"

    response = get(url=url)

    assert response.status_code == HTTPStatus.OK
    assert valid_likes_response(response.json())
