from collections.abc import Sequence
from typing import Any

from fastapi import APIRouter
from starlette import status

from core.database import SessionDep
from items.crud import (
    item_calculate_total_price,
    item_create,
    item_delete,
    item_read,
    item_read_all,
    item_update,
    items_filter_by_owner_id,
)
from items.model import (
    Item,
    ItemBase,
    ItemCreate,
    ItemRead,
    ItemReadShort,
    ItemUpdate,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: int, session: SessionDep) -> ItemRead:
    return item_read(item_id, session)


@router.post("/{item_id}", status_code=status.HTTP_202_ACCEPTED)
def create_item(item_in: ItemCreate, session: SessionDep) -> ItemBase:
    return item_create(item_in, session)


@router.get("/", status_code=status.HTTP_200_OK)
def read_all_items(session: SessionDep) -> list[ItemReadShort]:
    return item_read_all(session)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int, session: SessionDep) -> str:
    return item_delete(item_id, session)


@router.patch("/{item_id}", status_code=status.HTTP_200_OK)
def update_item(item_id: int, item_in: ItemUpdate, session: SessionDep) -> Item:
    return item_update(item_id, item_in, session)


@router.get("/get_by_owner/{owner_id}", status_code=status.HTTP_200_OK)
def get_items_by_owner(owner_id: int, session: SessionDep) -> Sequence[Any]:
    return items_filter_by_owner_id(owner_id, session)


@router.post("/calculate-total/", status_code=status.HTTP_202_ACCEPTED)
def item_calculate_total(item_ids: list[int], session: SessionDep) -> float:
    return item_calculate_total_price(item_ids, session)
