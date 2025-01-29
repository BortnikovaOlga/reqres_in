import pytest
from app.database.users_db_service import UserDBService
from app.model.user import UserData
from json_loader import load_json


@pytest.fixture(scope="session")
def insert_users(_db_engine_):
    """вставляет в БД записи из файла."""
    data = load_json("app/users.json")
    assert len(data)
    users_list = [UserData(**user) for user in data]
    for user in users_list:
        """убрать ид юзеров, чтобы не было конфликтов во время insert в бд"""
        user.id = None
    service = UserDBService(_db_engine_)
    return service.insert_users(users_list)
