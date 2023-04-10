conn = new Mongo();
db = conn.getDB("ugc2_movies");

db.createCollection("liked_films");
db.createCollection("bookmarks_films");
db.createCollection("reviewed_films");
