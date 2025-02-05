import random
from http import HTTPStatus
import pytest
import requests
from app.model.user import UserCreate


@pytest.mark.usefixtures("app_url")
class TestDeleteUser:
    path = "/api/users"

    def test_delete_user_by_id(self, insert_users, db_service):
        """Удалить пользователя по ид. (ид рандомное из вставленных в БД)
        Проверки :
        - КО 200 ОК,
        - в БД нет записи с ид удаленнного пользователя.
       """
        user = random.choice(insert_users)
        response = requests.delete(f"{self.app_url}{self.path}/{user.id}")
        assert response.status_code == HTTPStatus.OK
        assert db_service.get_user(user.id) is None

    def test_post_delete_get_user(self):
        """
        1. Создание пользователя, проверка КО 200 ОК
        2. Удаление пользователя, проверка КО 200 ОК
        3. Поиск по ид, КО 404
        """
        user_create = UserCreate.random()
        response = requests.post(f"{self.app_url}{self.path}", json=user_create.model_dump())
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        id = body["id"]

        response = requests.delete(f"{self.app_url}{self.path}/{id}")
        assert response.status_code == HTTPStatus.OK

        response = requests.get(f"{self.app_url}{self.path}/{id}")
        assert response.status_code == HTTPStatus.NOT_FOUND
