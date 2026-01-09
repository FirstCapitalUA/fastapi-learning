import json
import os

DATABASE_PATH = "data.json"

DEFAULT_DATA = {"users": {}, "items": {}}


def ensure_file_exists(path=DATABASE_PATH):
    """Создаёт файл, если он не существует."""
    if not os.path.exists(path):  # noqa: PTH110
        print("Файл не найден. Создаём новый файл...")
        write_json(DEFAULT_DATA, path)


def read_json(path=DATABASE_PATH):
    """Читает JSON-файл и возвращает данные как словарь."""
    ensure_file_exists(path)

    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Файл поврежден. Пересоздаём файл...")
        write_json(DEFAULT_DATA, path)
        return DEFAULT_DATA


def write_json(data, path=DATABASE_PATH):
    """Записывает данные (словарь/список) в JSON-файл."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
