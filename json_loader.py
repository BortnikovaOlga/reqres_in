import json


def load_json(filename):
    """
    Преобразует JSON-строку из файла в словарь с ключами ид пользователей.

    :param filename: Имя файла с JSON-строкой
    :return: Словареь или None в случае ошибки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file_data = file.read()
            json_data = json.loads(file_data)
            return {user["id"]: user for user in json_data}
    except (TypeError, ValueError, IOError) as e:
        print(f"Ошибка при чтении JSON из файла или преобразовании в словарь: {e}")
        return {}
