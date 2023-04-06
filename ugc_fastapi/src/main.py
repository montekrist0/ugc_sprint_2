from fastapi import FastAPI
import uvicorn


app = FastAPI(
    title="API для получения UGC",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    description="...",
    version="1.0.0",
)


# app.include_router(, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
