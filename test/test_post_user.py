from http import HTTPStatus
import pytest
from app.model.user import UserCreate, UserData


class TestCreateUser:
    path = "/api/users"

    def test_post_user(self, db_service, users_api):
        """Создать пользователя.
        Проверки :
        - КО 200 ОК,
        - в ответе данные соответствуют данным запроса
        - ид в ответе не пуст
        - в БД данные соответствуют данным запроса."""
        user_create = UserCreate.random()
        response = users_api.post(json=user_create.model_dump())
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        user_response = UserCreate.model_validate(body)
        assert user_response == user_create
        user_id = body["id"]
        assert user_id
        assert db_service.get_user(user_id) == UserData(**body)
        db_service.delete_user(user_id)

    @pytest.mark.parametrize("field_name", ["first_name", "last_name", "email", "avatar"])
    def test_post_user_with_empty_one_field(self, field_name, users_api):
        """Негативная проверка - пользователь не создается, если обязательное поле пусто."""
        user_create = UserCreate.random()
        setattr(user_create, field_name, None)
        response = users_api.post(json=user_create.model_dump())
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
