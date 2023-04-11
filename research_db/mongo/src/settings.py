from enum import Enum

CONNECTION_STRING = "mongodb://root:example@localhost:27017/"
FILM_COUNT = 100000
USERS_COUNT = 1000000
MIN_NUMBER_OF_PERSON_LIKES = 0
MAX_NUMBER_OF_PERSON_LIKES = 20
user_ids_filename = r"user_ids"
film_ids_filename = r"film_ids"
DB_NAME = "test_database"


class Collections(str, Enum):
    likes = "likes"
    reviews = "reviews"
    bookmarks = "bookmarks"
