from pydantic import EmailStr
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from items.model import ItemReadShort


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    password: str | None = Field(None, min_length=6, max_length=25)
    sex: str


# 2) покупать вещи, с добавлением items  и отниманием денег в балансе
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cart_id: int | None = None
    balance: float = Field(default=0.0)


class UserRead(UserBase):
    id: int
    balance: int


class UserCreate(UserBase):
    balance: int


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    age: int | None = None
    password: str | None = Field(None, min_length=6, max_length=25)
    sex: str | None = None
    balance: int | None = None


class UserReadShort(SQLModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserWithItems(UserReadShort):
    items: list[ItemReadShort]


class UserCart(SQLModel):
    user_id: int
    item_ids: list[int] | None = Field(default=None, sa_column=Column(JSON))


class UserCartCreate(UserCart):
    pass


# Добавляем table=True и первичный ключ
class UserCartRead(UserCart, table=True):
    id: int | None = Field(default=None, primary_key=True)
