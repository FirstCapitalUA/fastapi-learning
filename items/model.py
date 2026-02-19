from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    name: str
    description: str
    price: int
    quantity_in_stock: int
    adult_product: bool


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    quantity_in_stock: int | None = None
    owner_id: int | None = None
    # adult_product we don't want change this


class ItemReadShort(SQLModel):
    id: int
    name: str
    price: int
    adult_product: bool


class ItemRead(ItemBase):
    id: int
