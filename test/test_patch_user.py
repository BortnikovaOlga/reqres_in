from http import HTTPStatus
import pytest
from app.model.user import UserData, UserUpdate, UserCreate


class TestUpdateUser:

    @pytest.fixture()
    def created_user(self, users_api):
        """Предусловие - создать пользователя (через api), постусловие - удалить рользователя (через api)."""
        user_create = UserCreate.random()
        response = users_api.post(json=user_create.model_dump())
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        user = UserData.model_validate(body)
        yield user
        response = users_api.delete(user.id)
        assert response.status_code == HTTPStatus.OK

    def test_patch_user(self, created_user, db_service, users_api):
        """обновить все поля.
         Проверки :
         - КО 200 ОК,
         - в ответе данные обновлены.
         - в БД данные обновлены"""
        user_update = UserUpdate.random()
        response = users_api.patch(created_user.id, json=user_update.model_dump())
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert UserUpdate.model_validate(body) == user_update
        assert db_service.get_user(body["id"]) == UserData(**body)

    @pytest.mark.parametrize("attr_name", ["first_name", "last_name", "email", "avatar"])
    def test_patch_user_(self, created_user, attr_name, users_api):
        """обновить только одно поле.
        Проверки :
         - КО 200 ОК,
         - в ответе данные обновлены"""
        user_update = UserUpdate.random()
        attr_update = {attr_name: str(getattr(user_update, attr_name))}
        expected_user = UserData(**created_user.model_dump())
        setattr(expected_user, attr_name, attr_update[attr_name])

        response = users_api.patch(created_user.id, json=attr_update)
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        user_response = UserData.model_validate(body)
        assert user_response == expected_user

    @pytest.mark.parametrize("field_name", ["email", "avatar"])
    def test_patch_user_with_invalid_data(self, created_user, field_name, users_api):
        """Негативная проверка, обновить, когда одно обязательное поле не заполнено."""
        user_update = UserUpdate.random()
        setattr(user_update, field_name, "")
        response = users_api.patch(created_user.id, json=user_update.model_dump())
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
