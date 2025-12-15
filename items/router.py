
from fastapi import APIRouter
from starlette import status

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
    ItemCreate,
    ItemRead,
    ItemReadShort,
    ItemsTotal,
    ItemUpdate,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: int) -> Item | None:
    return item_read(item_id)


@router.post("/{item_id}", status_code=status.HTTP_202_ACCEPTED)
def create_item(item_in: ItemCreate) -> Item:
    return item_create(item_in)


@router.get("/", status_code=status.HTTP_200_OK)
def read_all_items() -> list[ItemReadShort]:
    return item_read_all()


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int) -> str:
    return item_delete(item_id)


@router.patch("/{item_id}", status_code=status.HTTP_200_OK)
def update_item(item_id: int, item_in: ItemUpdate) -> Item:
    return item_update(item_id, item_in)


@router.get("/get_by_owner/{owner_id}", status_code=status.HTTP_200_OK)
def get_items_by_owner(owner_id: int) -> list[ItemRead]:
    return items_filter_by_owner_id(owner_id)


@router.post("/calculate-total/", status_code=status.HTTP_202_ACCEPTED)
def calculate_cart_total(item_ids: list[int]) -> ItemsTotal:
    """
     мы получаем ид 1 и более итемов , суммируем их между собой и отправляем обратно результат.
     - Для этого мы создаем функцию которая будет находить итем_ид в имтемс. Если ид есть
     *добавляем* в **список**. Далее все что находится в списке мы сумируем между собой и возвращаем сумму
    :param ids: ids  для подсчета суммы
    :return: общая стоимость
    """
    total_sum = item_calculate_total_price(item_ids)
    return ItemsTotal(total=total_sum)
