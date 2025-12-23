from fastapi import APIRouter
from starlette import status

from core.database import SessionDep
from users.crud import (
    user_create,
    user_create_cart,
    user_delete,
    user_delete_cart,
    user_read,
    user_read_all,
    user_read_cart,
    user_update,
    user_with_items_model,
)
from users.model import (
    UserCart,
    UserCartCreate,
    UserCartRead,
    UserCreate,
    UserRead,
    UserReadShort,
    UserUpdate, User,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, session: SessionDep) -> UserRead:
    return user_read(user_id, session)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, session:SessionDep) -> UserCreate:
    return user_create(user_in, session)


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_in: UserUpdate, session:SessionDep) -> User:
    return user_update(user_id, user_in, session)


@router.get("/", status_code=status.HTTP_200_OK)
def read_all_users(session:SessionDep) -> list[UserReadShort]:
    return user_read_all(session)


@router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_user(user_id: int, session:SessionDep) -> str:
    return user_delete(user_id, session)


@router.get("/with_items/{user_id}", status_code=status.HTTP_200_OK)
def get_user_with_items_(user_id: int):
    return user_with_items_model(user_id)


@router.post("/{user_id}/cart", status_code=status.HTTP_201_CREATED)
def create_user_cart(user_cart_in: UserCartCreate) -> UserCartRead | None:
    """
    создать корзину с товарами для пользоавателя. У пользователя может быть только 1 корзина или не быть ее.
    корзина содержит ид пользователя и список ид предметов. Создать схему корзина и обновить схему юзер
    """
    return user_create_cart(user_cart_in)


@router.get("/{user_id}/cart", status_code=status.HTTP_200_OK)
def get_user_cart(user_id: int) -> UserCart:
    """
    получить корзину с товарами для пользоавателя.
    """
    return user_read_cart(user_id)


@router.delete("/{user_id}/cart", status_code=status.HTTP_202_ACCEPTED)
def delete_user_cart(user_id: int) -> str:
    """
    удалить корзину с товарами для пользоавателя.
    """
    return user_delete_cart(user_id)

