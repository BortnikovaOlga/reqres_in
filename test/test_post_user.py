from http import HTTPStatus

import pytest
import requests

from app.model.user import UserCreate


@pytest.mark.usefixtures("app_url")
class TestCreateUser:
    path = "/api/users"

    def test_post_user(self):
        user_create = UserCreate.random()
        response = requests.post(f"{self.app_url}{self.path}", json=user_create.model_dump())
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        user_response = UserCreate.model_validate(body)
        assert user_response == user_create
        user_id = body["id"]
        assert user_id
        requests.delete(f"{self.app_url}{self.path}/{user_id}")

    @pytest.mark.parametrize("field_name", ["first_name", "last_name", "email", "avatar"])
    def test_post_user_with_empty_one_field(self, field_name):
        user_create = UserCreate.random()
        setattr(user_create, field_name, None)
        response = requests.post(f"{self.app_url}{self.path}", json=user_create.model_dump())
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
