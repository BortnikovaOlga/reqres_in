from http import HTTPStatus

import pytest
import requests

from app.model.user import UserData, UserCreate


@pytest.mark.usefixtures("app_url")
class TestDeleteUser:
    path = "/api/users"

    def test_delete_user(self):
        user_create = UserCreate.random()
        response = requests.post(f"{self.app_url}{self.path}", json=user_create.model_dump())
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        id = body["id"]

        response = requests.delete(f"{self.app_url}{self.path}/{id}")
        assert response.status_code == HTTPStatus.OK

        response = requests.get(f"{self.app_url}{self.path}/{id}")
        assert response.status_code == HTTPStatus.NOT_FOUND
