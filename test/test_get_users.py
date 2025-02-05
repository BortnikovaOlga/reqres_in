import random
from http import HTTPStatus

import pytest
import requests

from app.model.user import UserData, UserCreate, UsersDataPage


@pytest.mark.usefixtures("app_url")
class TestGetUsers:
    path = "/api/users"

    @pytest.fixture()
    def created_user(self):
        """Предусловие - создать пользователя (через api), постусловие - удалить рользователя (через api)."""
        user_create = UserCreate.random()
        response = requests.post(f"{self.app_url}{self.path}", json=user_create.model_dump())
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        user = UserData.model_validate(body)
        yield user
        response = requests.delete(f"{self.app_url}{self.path}/{user.id}")
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.smoke
    @pytest.mark.usefixtures("insert_users")
    def test_get_all_users(self, db_service):
        """Получить всех пользователей (пользователи уже созданы в БД - в фикстуре).
        Проверки :
         - КО 200 ОК,
         - количество пользователей в ответе совпадает с числом пользователей в массиве,
         - поле total содержит то же число. """
        response = requests.get(f"{self.app_url}{self.path}")
        assert response.status_code == HTTPStatus.OK
        page_data = UsersDataPage.model_validate(response.json())
        db_users = db_service.get_users()
        assert set([user.id for user in page_data.items]) == set([user.id for user in db_users])

    def test_get_user_by_id(self, insert_users):
        """Получить пользователя по ид. (ид рандомное из вставленных в БД)
        Проверки :
        - КО 200 ОК,
        - в ответе поля page, size содержат числа из параметров запроса
        - количество пользователей по формуле, в зависимости от получаемой страницы"""
        user = random.choice(insert_users)
        response = requests.get(f"{self.app_url}{self.path}/{user.id}")
        assert response.status_code == HTTPStatus.OK
        response_user = UserData.model_validate(response.json())
        assert response_user == user

    def test_get_user_by_id_(self, created_user):
        """Получить пользователя по ид пользователя. (Пользователь создан через апи в фикстре)
        Проверки :
        - КО 200 ОК,
        - в ответе поля page, size содержат числа из параметров запроса
        - количество пользователей по формуле, в зависимости от получаемой страницы"""
        response = requests.get(f"{self.app_url}{self.path}/{created_user.id}")
        assert response.status_code == HTTPStatus.OK
        user = UserData.model_validate(response.json())
        assert user.id == created_user.id

    @pytest.mark.parametrize("user_id", [100000000000000])
    def test_get_user_by_not_exist_id(self, user_id):
        """Получить пользователя с несуществующим ид."""
        response = requests.get(f"{self.app_url}{self.path}/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [-10, 0, "one"])
    def test_get_user_by_invalid_id(self, user_id):
        """Запрос пользователя с невалидным ид."""
        response = requests.get(f"{self.app_url}{self.path}/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
