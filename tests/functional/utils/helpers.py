from schema import And, Schema, SchemaError


def valid_likes_response(body: dict):
    schema = Schema(
        [
            {
                "id": And(str, lambda param: param != ""),
                "film_id": And(str, lambda param: param != ""),
                "user_id": And(str, lambda param: param != ""),
                "rating": And(int),
            }
        ]
    )
    try:
        schema.validate(body)
        return True
    except SchemaError:
        return False


def valid_bookmarks_response(body: dict):
    schema = Schema(
        [
            {
                "id": And(str, lambda param: param != ""),
                "film_id": And(str, lambda param: param != ""),
                "user_id": And(str, lambda param: param != ""),
                "created": And(str, lambda param: param != ""),
            }
        ]
    )
    try:
        schema.validate(body)
        return True
    except SchemaError:
        return False


def valid_reviews_response(body: dict):
    schema = Schema(
        [
            {
                "id": And(str, lambda param: param != ""),
                "film_id": And(str, lambda param: param != ""),
                "user_id": And(str, lambda param: param != ""),
                "liked_films_id": And(str, lambda param: param != ""),
                "text": And(str, lambda param: param != ""),
                "ratings": list,
                "avg_rating_review": And(float),
                "created": And(str, lambda param: param != ""),
            }
        ]
    )
    try:
        schema.validate(body)
        return True
    except SchemaError:
        return False
