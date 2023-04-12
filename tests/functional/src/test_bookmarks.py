import random
from http import HTTPStatus

from requests import get

from tests.functional.settings import settings
from tests.functional.utils.helpers import valid_bookmarks_response


def test_get_users_bookmarks(user_ids):
    user_id = random.choice(user_ids)
    url = f"{settings.service_url}/api/v1/bookmarks/users/{user_id}"

    response = get(url=url, json={})

    assert response.status_code == HTTPStatus.OK
    assert valid_bookmarks_response(response.json())
