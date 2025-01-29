import json


def load_json(filename):
    """
    Преобразует JSON-строку из файла в список пользователей.

    :param filename: Имя файла с JSON-строкой
    :return: Список или None в случае ошибки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file_data = file.read()
            return json.loads(file_data)

    except (TypeError, ValueError, IOError) as e:
        print(f"Ошибка при чтении JSON из файла или преобразовании в словарь: {e}")
        return {}
