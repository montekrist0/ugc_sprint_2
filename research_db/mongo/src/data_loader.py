import pickle
import random

from pymongo.database import Collection
from pymongo.errors import CollectionInvalid
from tqdm import tqdm

from src.data_generator import DataGenerator
from src.db_manager import MongoDBManager
import src.settings as settings


def get_ids(filename: str, count: int):
    """
    Функция достает из файла список id. Если файла нет - создает список и сохраняет в файл.

    :param filename: Имя файла, в который будет сохранен список id фильмов, пользователей или прочих объектов
    :param count: количество id для генерации
    :return:
    """
    dg = DataGenerator()
    ids = []

    try:
        with open(filename, "rb") as file:
            ids = pickle.load(file)

    except FileNotFoundError:
        ids = dg.gen_ids(count)
        with open(filename, "wb") as file:
            pickle.dump(ids, file)

    finally:
        return ids


user_ids = get_ids(settings.user_ids_filename, settings.USERS_COUNT)
film_ids = get_ids(settings.film_ids_filename, settings.FILM_COUNT)


def get_random_film_ids(film_list: list, film_count):
    """

    :param film_list: список id фильмов
    :param film_count: количество рандомных id фильмов, которые требуется вернуть
    :return:
    """
    start_index = random.randint(0, settings.FILM_COUNT - film_count - 1)
    for i in range(start_index, start_index + film_count):
        yield film_list[i]


def generate_likes(collection: Collection, u_ids: list, f_ids: list):
    """
    Функция создает рандомные документы в переданной коллекции

    :param f_ids: список id фильмов
    :param collection: коллекция в MongoDB
    :param u_ids: список id пользователей
    :return:
    """

    dg = DataGenerator()

    for user_id in tqdm(u_ids):
        user_film_count = random.randint(settings.MIN_NUMBER_OF_PERSON_LIKES, settings.MAX_NUMBER_OF_PERSON_LIKES)
        if user_film_count:
            collection.insert_many(
                [
                    dg.generate_like_doc(user_id=user_id, film_id=film_id)
                    for film_id in get_random_film_ids(film_list=f_ids, film_count=user_film_count)
                ]
            )


def main():
    mongodb_manager = MongoDBManager(settings.CONNECTION_STRING, settings.DB_NAME)

    try:
        like_collection = mongodb_manager.create_collection(settings.Collections.likes)
    except CollectionInvalid:
        like_collection = mongodb_manager.db.get_collection(settings.Collections.likes)

    generate_likes(like_collection, user_ids, film_ids)

    like_collection.create_index([("film_id", 1)])
    like_collection.create_index([("user_id", 1)])


if __name__ == "__main__":
    main()
