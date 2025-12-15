users: dict[int, dict[str, str | int]] = {
    1: {
        "first_name": "John",
        "last_name": "Doe",
        "email": "jehn.doe@gmail.com",
        "age": 25,
        "password": "qwerty234",
        "sex": "Male",
    },
    2: {
        "first_name": "Jonny",
        "last_name": "Dobe",
        "email": "jonny.dobe@gmail.com",
        "age": 27,
        "password": "qwerty123",
        "sex": "Male",
    },
    3: {
        "first_name": "Donny",
        "last_name": "Joui",
        "email": "donny.joui@gmail.com",
        "age": 32,
        "password": "qwtyqwqw23",
        "sex": "Male",
    },
    4: {
        "first_name": "Jerny",
        "last_name": "Dope",
        "email": "jerny.dope@gmail.com",
        "age": 27,
        "password": "qwertwy1223",
        "sex": "Male",
    },
    5: {
        "first_name": "Tanny",
        "last_name": "Arty",
        "email": "tanny.arty@gmail.com",
        "age": 22,
        "password": "qwer2ty1w23",
        "sex": "Female",
    },
}

items: dict[int, dict[str, str | int]] = {
    1: {
        "name": "ball",
        "description": "beautiful white ball",
        "price": 50,
        "quantity_in_stock": 5,
    },
    2: {
        "name": "stick",
        "description": "The most successful of all clubs",
        "price": 150,
        "quantity_in_stock": 8,
    },
    3: {
        "name": "snowboard",
        "description": "Very comfortable snowboard",
        "price": 390,
        "quantity_in_stock": 4,
    },
    4: {
        "name": "bicycle",
        "description": "Fast and inexpensive bike",
        "price": 500,
        "quantity_in_stock": 2,
    },
}
# словарь с items

# словарь имеет ключи и значения. Значениями может бьіть любой тип. Ключом может бьіть только неизменяемьій тип
# ключи словаря могут бьіть int i str, булевьіе значения. Ключи не могут дублироваться. Тру 1 значение ,
# фолс 2 , нон 3е значение kортеж. строки - неизменяемьій тип. (обьект)
