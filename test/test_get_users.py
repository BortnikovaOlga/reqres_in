import random
from http import HTTPStatus
from typing import List
import pytest
from pydantic import TypeAdapter
from app.model.user import UserData, UserCreate


class TestGetUsers:

    @pytest.fixture()
    def created_user(self, users_api):
        """Предусловие - создать пользователя (через api), постусловие - удалить пользователя (через api)."""
        user_create = UserCreate.random()
        response = users_api.post(json=user_create.model_dump())
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        user = UserData.model_validate(body)
        yield user
        response = users_api.delete(user.id)
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.smoke
    @pytest.mark.usefixtures("insert_users")
    def test_get_all_users(self, db_service, users_api):
        """Получить всех пользователей (пользователи уже созданы в БД - в фикстуре).
        Проверки :
         - КО 200 ОК,
         - множества ид пользователей (из респонза и из запроса к бд) - совпадают,
         """
        response = users_api.get_all()
        assert response.status_code == HTTPStatus.OK
        json = response.json()
        data = TypeAdapter(List[UserData]).validate_python(json)

        db_users = db_service.get_users()

        assert set([user.id for user in data]) == set([user.id for user in db_users])

    def test_get_user_by_id(self, insert_users, users_api):
        """Получить пользователя по ид. (ид рандомное из вставленных в БД)
        Проверки :
        - КО 200 ОК,
        - пользователь из ответа совпадает с рандомно выбранным из бд.
        """
        user = random.choice(insert_users)
        response = users_api.get_by_id(user.id)
        assert response.status_code == HTTPStatus.OK
        response_user = UserData.model_validate(response.json())
        assert response_user == user

    def test_get_user_by_id_(self, created_user, users_api):
        """Получить пользователя по ид пользователя. (Пользователь создан через апи в фикстре)
        Проверки :
        - КО 200 ОК,
        - в ответе пользователь , который создан в предусловиях."""
        response = users_api.get_by_id(created_user.id)
        assert response.status_code == HTTPStatus.OK
        user = UserData.model_validate(response.json())
        assert user == created_user

    @pytest.mark.parametrize("user_id", [100000000000000])
    def test_get_user_by_not_exist_id(self, user_id, users_api):
        """Получить пользователя с несуществующим ид."""
        response = users_api.get_by_id(user_id)
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [-10, 0, "one"])
    def test_get_user_by_invalid_id(self, user_id, users_api):
        """Запрос пользователя с невалидным ид."""
        response = users_api.get_by_id(user_id)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
