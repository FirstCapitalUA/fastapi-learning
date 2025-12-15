from typing import Any

from fastapi import HTTPException

from helper.files import read_json, write_json
from items.model import Item, ItemCreate, ItemRead, ItemReadShort, ItemUpdate


def _load_items() -> dict[int, dict]:
    db = read_json()
    items = db.get("items", {})
    return {int(k): v for k, v in items.items()}


def _save_items(items: dict[int, dict]):
    # Convert keys back to str for JSON compatibility
    db = read_json()
    db["items"] = {str(k): v for k, v in items.items()}
    write_json(db)


def item_create(item_in: ItemCreate) -> Item:
    items = _load_items()

    # новый ID
    new_id = max(items.keys(), default=0) + 1

    item = Item(**item_in.model_dump())
    items[new_id] = item.model_dump()

    _save_items(items)

    return item


def item_read(item_id: int) -> ItemRead | HTTPException:
    items = _load_items()
    item_data = items.get(item_id)

    if not item_data:
        msg = f"Item {item_id} is not found."
        return HTTPException(status_code=404, detail=msg)

    return ItemRead(id=item_id, **item_data)


def item_read_all() -> list[ItemReadShort]:
    items = _load_items()
    return [ItemReadShort(**data) for data in items.values()]


def item_delete(item_id: int) -> HTTPException | str:
    items = _load_items()

    if item_id not in items:
        msg = f"Item {item_id} is not found."
        return HTTPException(status_code=404, detail=msg)
    del items[item_id]
    _save_items(items)
    return f"Предмет с id {item_id} удален"


def item_update(item_id: int, item_in: ItemUpdate) -> ItemRead:
    items = _load_items()

    if item_id not in items:
        msg = f"Item {item_id} is not found."
        raise HTTPException(status_code=404, detail=msg)

    current_item_data = items[item_id]
    update_data = item_in.model_dump(exclude_unset=True)

    current_item_data.update(update_data)
    items[item_id] = current_item_data

    _save_items(items)

    return ItemRead(id=item_id, **current_item_data)


def items_filter_by_owner_id(owner_id: int) -> list[ItemRead]:
    items = _load_items()
    owner_data = []
    for key, value in items.items():
        if value["owner_id"] == owner_id:
            owner_data.append(ItemRead(id=key, **value))
    return owner_data


def item_calculate_total_price(ids: list[int]) -> HTTPException | float | Any:
    """
     мы получаем ид 1 и более итемов , суммируем их между собой и отправляем обратно результат.
     Для этого мы создаем функцию которая будет находить итем_ид в имтемс. Если ид есть
     добавляем в список. Далее все что находится в списке мы сумируем между собой и возвращаем сумму
    :param ids: ids  для подсчета суммы
    :return: общая стоимость
    """
    total_sum = 0.0
    items = _load_items()

    for item_id in ids:
        if item_id not in items:
            msg = f"Item {item_id} is not found."
            return HTTPException(status_code=404, detail=msg)
        item_data = items[item_id]
        price = item_data.get("price", 0.0)
        total_sum += price
    return total_sum
