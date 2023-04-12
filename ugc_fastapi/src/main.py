from fastapi import FastAPI
import uvicorn

from db.clients import mongo
from view.api.v1 import user_films_like, bookmark, review

app = FastAPI(
    title="API для получения UGC",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    description="...",
    version="1.0.0",
)


app.include_router(user_films_like.router, prefix="/api/v1/likes", tags=["Likes"])
app.include_router(bookmark.router, prefix="/api/v1/bookmarks", tags=["Bookmarks"])
app.include_router(review.router, prefix="/api/v1/reviews", tags=["Reviews"])


@app.on_event("startup")
def startup():
    mongo.client = mongo.create_mongo_client()


@app.on_event("shutdown")
def shutdown():
    mongo.client.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
