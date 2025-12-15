from fastapi import HTTPException

from helper.files import read_json, write_json
from items.crud import _load_items
from users.model import (
    User,
    UserCartCreate,
    UserCartRead,
    UserCreate,
    UserRead,
    UserReadShort,
    UserUpdate,
    UserWithItems,
)


def _load_users() -> dict[int, dict]:
    db = read_json()
    users = db.get("users", {})
    return {int(k): v for k, v in users.items()}


def _save_users(users: dict[int, dict]):
    db = read_json()
    db["users"] = {str(k): v for k, v in users.items()}
    write_json(db)


def _load_cart() -> dict[int, dict]:
    db = read_json()
    cart = db.get("cart", {})
    return {int(k): v for k, v in cart.items()}


def _save_cart(cart: dict[int, dict]):
    db = read_json()
    db["cart"] = {str(k): v for k, v in cart.items()}
    write_json(db)


def user_create(user_in: UserCreate) -> User:
    users = _load_users()
    new_id = max(users.keys(), default=0) + 1
    user = User(**user_in.model_dump())
    users[new_id] = user.model_dump()
    _save_users(users)
    return user


def user_read_all() -> list[UserReadShort]:
    users = _load_users()
    return [UserReadShort(id=i, **data) for i, data in users.items()]


def user_read(user_id: int) -> HTTPException | UserRead:
    users = _load_users()
    user_data = users.get(user_id)
    if not user_data:
        msg = f"user {user_id} is not found."
        return HTTPException(status_code=404, detail=msg)
    return UserRead(id=user_id, **user_data)

def user_update(user_id: int, user_in: UserUpdate) -> UserRead:
    users = _load_users()
    if user_id not in users:
        msg = f"user {user_id} is not found."
        raise HTTPException(status_code=404, detail=msg)

    current_data = users[user_id]
    update_data = user_in.model_dump(exclude_unset=True)
    current_data.update(update_data)
    users[user_id] = current_data
    _save_users(users)
    return UserRead(id=user_id, **current_data)


def user_delete(user_id: int) -> HTTPException | str:
    users = _load_users()

    if user_id not in users:
        msg = f"user {user_id} is not found."
        return HTTPException(status_code=404, detail=msg)
    del users[user_id]
    _save_users(users)
    return f"Пользователь с id {user_id} удален"




def user_with_items_model(user_id: int) -> HTTPException | UserWithItems:
    users = _load_users()
    items = _load_items()

    if user_id not in users:
        msg = f"user {user_id} is not found."
        return HTTPException(status_code=404, detail=msg)


    user_data = users[user_id]

    user_items = []
    for item_id, details in items.items():
        if details.get("owner_id") == user_id:
            item_data = {"id": item_id, **details}
            user_items.append(item_data)

    return UserWithItems(id=user_id, items=user_items, **user_data)


def user_create_cart(cart_in: UserCartCreate) -> UserCartRead | None:
    carts = _load_cart()
    cart_id = max(carts.keys(), default=0) + 1
    cart_data = cart_in.model_dump()
    cart = UserCartRead(id=cart_id, **cart_data)
    carts[cart_id] = cart.model_dump()
    _save_cart(carts)
    return cart


def user_read_cart(user_id: int) -> HTTPException | UserCartRead:
    carts = _load_cart()

    cart_data = None

    for cart_details in carts.values():
        if cart_details.get("user_id") == user_id:
            cart_data = cart_details
            break

    if cart_data is None:
        msg = f"user {user_id} is not found."
        return HTTPException(status_code=404, detail=msg)

    return UserCartRead(**cart_data)


def user_delete_cart(user_id: int) -> str | None:
    carts = _load_cart()

    cart_delete = None

    for cart_id, cart_details in carts.items():
        if cart_details.get("user_id") == user_id:
            cart_delete = cart_id
            break

    if not cart_delete:
        msg = f"Корзина пользователя {user_id} не найдена."
        raise HTTPException(status_code=404, detail=msg)
    del carts[cart_delete]
    _save_cart(carts)

    return f"Корзина {user_id} успешно удалена."
