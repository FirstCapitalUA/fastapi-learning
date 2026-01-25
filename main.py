import uvicorn
from fastapi import FastAPI

from core.database import create_db_and_tables
from items.router import router as items_router
from users.router import router as users_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"Hello World"}


app.include_router(items_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
