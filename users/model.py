from pydantic import EmailStr

from items.model import ItemReadShort

from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    password: str | None = Field(None, min_length=6, max_length=25)
    sex: str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cart_id: int | None = None



class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    age: int | None = None
    password: str | None = Field(None, min_length=6, max_length=25)
    sex: str | None = None


class UserReadShort(SQLModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserWithItems(UserReadShort):
    items: list[ItemReadShort]


class UserCart(SQLModel):
    user_id: int
    item_ids: list[int] | None = None


class UserCartCreate(UserCart):
    pass


class UserCartRead(UserCart):
    id: int

