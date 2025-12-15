from pydantic import BaseModel, EmailStr, Field

from items.model import ItemReadShort


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    password: str | None = Field(None, min_length=6, max_length=25)
    sex: str
    cart_id: int | None = None


class UserRead(User):
    id: int


class UserCreate(User):
    pass


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    age: int | None = None
    password: str | None = Field(None, min_length=6, max_length=25)
    sex: str | None = None


class UserReadShort(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserWithItems(UserReadShort):
    items: list[ItemReadShort]


class UserCart(BaseModel):
    user_id: int
    item_ids: list[int] | None = None


class UserCartCreate(UserCart):
    pass


class UserCartRead(UserCart):
    id: int  # ид козины
