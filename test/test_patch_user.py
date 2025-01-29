from http import HTTPStatus

import pytest
import requests

from app.model.user import UserData, UserUpdate, UserCreate


@pytest.mark.usefixtures("app_url")
class TestUpdateUser:
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

    def test_patch_user(self, created_user):
        """обновить все поля."""
        user_update = UserUpdate.random()
        response = requests.patch(f"{self.app_url}{self.path}/{created_user.id}", json=user_update.model_dump())
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body["id"]
        user_response = UserUpdate.model_validate(body)
        assert user_response == user_update

    @pytest.mark.parametrize("attr_name", ["first_name", "last_name", "email", "avatar"])
    def test_patch_user_(self, created_user, attr_name):
        """обновить только одно поле."""
        user_update = UserUpdate.random()
        attr_update = {attr_name: str(getattr(user_update, attr_name))}
        expected_user = UserData(**created_user.model_dump())
        setattr(expected_user, attr_name, attr_update[attr_name])

        response = requests.patch(f"{self.app_url}{self.path}/{created_user.id}", json=attr_update)
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        user_response = UserData.model_validate(body)
        assert user_response == expected_user

    @pytest.mark.parametrize("field_name", ["email", "avatar"])
    def test_patch_user_with_invalid_data(self, created_user, field_name):
        """обновить все поля, одно поле невалидное."""
        user_update = UserUpdate.random()
        setattr(user_update, field_name, "")
        response = requests.patch(f"{self.app_url}{self.path}/{created_user.id}", json=user_update.model_dump())
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
