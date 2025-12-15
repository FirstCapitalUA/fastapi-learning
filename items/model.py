from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: int
    quantity_in_stock: int
    owner_id: int | None = None


class ItemCreate(Item):
    pass


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    quantity_in_stock: int | None = None
    owner_id: int | None = None


class ItemReadShort(BaseModel):
    name: str
    price: int


class ItemRead(Item):
    id: int


class ItemsTotal(BaseModel):
    total: float
