import json
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, select

from core.config import settings
from items.model import Item
from users.model import User

# для PostgreSQL:
# DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # только для SQLite
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def load_data_from_json(file_path: str):
    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)

    with Session(engine) as session:
        # 1. Загружаем пользователей
        if "users" in data:
            for user_data in data["users"]:
                # Проверяем, существует ли уже такой пользователь (по email)
                statement = select(User).where(User.email == user_data["email"])
                existing_user = session.exec(statement).first()

                if not existing_user:
                    db_user = User(**user_data)
                    session.add(db_user)

        # 2. Загружаем товары
        if "items" in data:
            for item_data in data["items"]:
                # Проверяем по названию (или другому уникальному полю)
                statement = select(Item).where(Item.name == item_data["name"])
                existing_item = session.exec(statement).first()

                if not existing_item:
                    db_item = Item(**item_data)
                    session.add(db_item)

        # Сохраняем все изменения в базе
        session.commit()
        print("Данные успешно загружены!")
