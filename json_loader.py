import json


def load_json(filename):
    """
    Преобразует JSON-строку из файла в список словарей.

    :param filename: Имя файла с JSON-строкой
    :return: Список словарей или None в случае ошибки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return {user["id"]: user for user in json.loads(file.read())}
    except (TypeError, ValueError, IOError) as e:
        print(f"Ошибка при чтении JSON из файла или преобразовании в словарь: {e}")
        return None
