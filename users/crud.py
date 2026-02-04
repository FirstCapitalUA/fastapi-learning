from fastapi import HTTPException
from sqlmodel import Session, select

from helper.files import read_json, write_json
from items.model import Item
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

ADULT_AGE = 18


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


def user_create(user_in: UserCreate, session: Session) -> UserCreate:
    user = User(**user_in.model_dump())
    session.add(user)  # Добавляем в сессию
    session.commit()  # Сохраняем в файл .db
    session.refresh(user)  # Получаем ID от базы
    return user_in


def user_read_all(session: Session) -> list[UserReadShort]:
    users = session.exec(select(User)).all()
    return [UserReadShort(**user.model_dump()) for user in users]


def user_read(user_id: int, session: Session) -> UserRead:
    user = session.get(User, user_id)
    if not user:
        msg = f"user {user_id} is not found."
        raise HTTPException(status_code=404, detail=msg)
    return UserRead(**user.model_dump())


def user_update(user_id: int, user_in: UserUpdate, session: Session) -> User:
    user: User | None = session.get(User, user_id)
    if not user:
        msg = f"user {user_id} is not found."
        raise HTTPException(status_code=404, detail=msg)

    update_data = user_in.model_dump(exclude_unset=True)

    user.sqlmodel_update(update_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def user_delete(user_id: int, session: Session) -> str:
    user = session.get(User, user_id)

    if not user:
        msg = f"user {user_id} is not found."
        raise HTTPException(status_code=404, detail=msg)
    session.delete(user)
    session.commit()
    return f"Пользователь с id {user_id} удален"


def user_with_items_model(user_id: int, session: Session) -> UserWithItems:
    users = session.get(User, user_id)
    if not users:
        msg = f"user {user_id} is not found."
        raise HTTPException(status_code=404, detail=msg)

    statement = select(Item).where(Item.owner_id == user_id)
    items = session.exec(statement).all()
    user_data = users.model_dump()
    user_data["items"] = items
    return UserWithItems(**user_data)


def user_create_cart(cart_in: UserCartCreate, session: Session) -> UserCartRead:
    # 1. Проверяем, существует ли пользователь
    user = session.get(User, cart_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {cart_in.user_id} not found")

    # 2. Проверяем, нет ли у него уже корзины (логика: 1 юзер = 1 корзина)
    statement = select(UserCartRead).where(UserCartRead.user_id == cart_in.user_id)
    cart = session.exec(statement).first()
    if cart:
        raise HTTPException(status_code=400, detail="User already has a cart")

    # 3. Создаем корзину
    db_cart = UserCartRead.model_validate(cart_in)
    session.add(db_cart)
    session.commit()
    session.refresh(db_cart)

    # 4. Опционально: обновляем поле cart_id в таблице User
    user.cart_id = db_cart.id
    session.add(user)
    session.commit()

    return db_cart


def user_read_cart(user_id: int, session: Session) -> UserCartRead:
    # Ищем в таблице Cart строку, где user_id совпадает
    statement = select(UserCartRead).where(UserCartRead.user_id == user_id)
    cart = session.exec(statement).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


def user_delete_cart(user_id: int, session: Session) -> dict[str, str]:
    statement = select(UserCartRead).where(UserCartRead.user_id == user_id)
    cart = session.exec(statement).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    user = session.get(User, user_id)
    if user:
        user.cart_id = None
        session.add(user)

    session.delete(cart)

    session.commit()

    return {"detail": f"Cart for user {user_id} successfully deleted"}


def user_buy_item(user_id: int, item_id: int, session: Session) -> dict:
    user = session.get(User, user_id)
    item = session.get(Item, item_id)

    if not user or not item:
        raise HTTPException(status_code=404, detail="User or Item not found")

    if user.balance < item.price:
        raise HTTPException(status_code=400, detail=f"Недостаточно средств. Нужно: {item.price}, у вас: {user.balance}")

    if item.adult_product and user.age < ADULT_AGE:
        raise HTTPException(status_code=400, detail=f"You are not yet {ADULT_AGE} years old")

    user.balance -= item.price

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "Покупка успешна", "new_balance": user.balance}


def user_buy_items_for_cart(user_id: int, session: Session) -> dict:  # Поменял на dict для удобства
    statement = select(UserCartRead).where(UserCartRead.user_id == user_id)
    cart = session.exec(statement).first()
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    if not cart.item_ids:
        raise HTTPException(status_code=400, detail="Cart is empty")

    items_statement = select(Item).where(Item.id.in_(cart.item_ids))
    items = session.exec(items_statement).all()

    total_price = sum(item.price for item in items)

    if user.balance < total_price:
        raise HTTPException(status_code=400, detail=f"Low balance: {total_price}, you have: {user.balance}")

    for item in items:
        if item.adult_product and user.age < ADULT_AGE:
            raise HTTPException(status_code=400, detail=f"You are not yet {ADULT_AGE} years old")

    user.balance -= total_price

    session.add(user)
    session.delete(cart)
    session.commit()

    session.refresh(user)

    return {"admin say": "order complete", "You new balance": user.balance}
