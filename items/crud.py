from collections.abc import Sequence
from typing import Any

from fastapi import HTTPException
from sqlmodel import Session, func, select

from items.model import Item, ItemCreate, ItemRead, ItemReadShort, ItemUpdate


def item_create(item_in: ItemCreate, session: Session) -> ItemCreate:
    item = Item(**item_in.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item_in  # TODO return db item


def item_read(item_id: int, session: Session) -> ItemRead | HTTPException:
    item = session.get(Item, item_id)
    if not item:
        msg = f"Item {item_id} is not found."
        return HTTPException(status_code=404, detail=msg)
    return ItemRead(**item.model_dump())


def item_read_all(session: Session) -> list[ItemReadShort]:
    items = session.exec(select(Item)).all()
    return [ItemReadShort(**item.model_dump()) for item in items]


def item_delete(item_id: int, session: Session) -> HTTPException | str:
    items = session.get(Item, item_id)
    if not items:
        msg = f"Item {item_id} is not found."
        return HTTPException(status_code=404, detail=msg)
    session.delete(items)
    session.commit()
    return f"Предмет с id {item_id} удален"


def item_update(item_id: int, item_in: ItemUpdate, session: Session) -> Item:
    item: Item | None = session.get(Item, item_id)

    if not item:
        msg = f"Item {item_id} is not found."
        raise HTTPException(status_code=404, detail=msg)

    update_data = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_data)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item


def items_filter_by_owner_id(owner_id: int, session: Session) -> Sequence[Any]:
    statement = select(Item).where(Item.owner_id == owner_id)

    items = session.exec(statement).all()

    if not items:
        raise HTTPException(status_code=404, detail=f"No items found for owner {owner_id}")

    return items


def item_calculate_total_price(ids: list[int], session: Session) -> float:
    statement = select(func.sum(Item.price)).where(Item.id.in_(ids))
    total = session.exec(statement).one()

    return total or 0.0
