import pytest
import requests
from http import HTTPStatus

from app.model.auth import LoginResponse
from auth_db import auth_db


@pytest.mark.usefixtures("app_url")
class TestLogin:
    path = "/api/login"

    @pytest.mark.smoke
    @pytest.mark.parametrize("login", auth_db.keys())
    def test_auth_with_valid_data(self, login):
        """Авторизация с валидным логином и паролем."""
        response = requests.post(f"{self.app_url}{self.path}", json={"email": login, "password": auth_db[login]})
        assert response.status_code == HTTPStatus.OK
        body = LoginResponse.validate(response.json())
        assert body.token

    @pytest.mark.parametrize("password", ["", " ", "cityslick"])
    @pytest.mark.parametrize("login", auth_db.keys())
    def test_auth_with_invalid_password(self, login, password):
        """Авторизация с невалидным паролем."""
        response = requests.post(f"{self.app_url}{self.path}", json={"email": login, "password": password})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize("login", ["", " ", "eve.holt"])
    def test_auth_with_invalid_login(self, login):
        """Авторизация с невалидным логином."""
        response = requests.post(f"{self.app_url}{self.path}", json={"email": login, "password": "password"})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize("auth_data", [{"email": "", "password": ""}, {"email": " ", "password": " "}])
    def test_auth_with_invalid_login_password(self, auth_data):
        """Авторизация с пустыми логином/паролем."""
        response = requests.post(f"{self.app_url}{self.path}", json=auth_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize("auth_data", [{"email": "1@1.ru"}, {"password": "password"}])
    def test_auth_with_invalid_data(self, auth_data):
        """Авторизация с невалидной структурой запроса - отсутствует логин или пароль."""
        response = requests.post(f"{self.app_url}{self.path}", json=auth_data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
