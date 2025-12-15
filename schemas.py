from pydantic import BaseModel

fruits_data = [
    {"name": "apple"},
    {"name": "banana"},
    {"name": "orange"},
]


class Fruit(BaseModel):
    name: str


class Vegetable(BaseModel):
    name: str


class Bucket(Fruit):
    objects: list[Fruit | Vegetable]


fruits_classes = []
for f in fruits_data:
    fr_cls = Fruit(**f)
    fruits_classes.append(fr_cls)

vegetables_classes = [Vegetable(name="tomato")]

fruit_bucket = Bucket(objects=fruits_classes)
print(fruit_bucket)

bucket_2 = Bucket(objects=vegetables_classes)


# all_cars = [
#     {"name": "leissan, electrick"},
#     {"name": "audi, 3.2"},
#     {"name": "VAZ, 1.6"},
#     {"name": "dodgee, 6.8"},
#     {"name": "ford, 4.0"},
#     {"name": "buick, 7.8"},
#
# ]
# class Cars(BaseModel):
#     name: str
#
#
# class Car_amer(BaseModel):
#     name: str
#     objects: list[Cars]
#
#
# auto_classes = []
# for c in all_cars:
#     car_cls = Cars(**c)
#     auto_classes.append(car_cls)
#
# china_auto = [Cars(name="leissan, electrick")]
#
# amer_cars = Car_amer(name="usa", objects=auto_classes)
# print(amer_cars)
#
# chin_cars_2 = Car_amer(name="china", objects=china_auto)
# print(chin_cars_2)
