import uvicorn
from fastapi import FastAPI

from items.router import router as items_router
from users.router import router as users_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello Dmitriy"}


app.include_router(items_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104


# Сделать связь между пользователями и итемами.
