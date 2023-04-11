# Описание схемы хранения данных в коллекциях

### LIKES

```json lines
{
  "film_id": "film_id_1",
  "user_id": "user_id_1",
  "rating": 5
}
```

### REVIEWS

```json lines

{
  "film_id": "film_id_1",
  "user_id": "user_id_1",
  "user_films_like_id": "some_object_id",
  "text": "great movie",
  "ratings": [
    {
      "user_id": "some_user_id",
      "rating": 4
    }
  ],
  "avg_rating_review": 5.7,
  "created": "some_date"
}
```

### BOOKMARKS

```json lines
{
  "user_id": "user_id",
  "film_id": "film_id",
  "created": "some_date"
}
```