import pytest
import requests

from auth_db import auth_db


class TestLogin:
    url = f"http://127.0.0.1:8080/api/login"

    @pytest.mark.parametrize("login", auth_db.keys())
    def test_auth_with_valid_data(self, login):
        """Авторизация с валидным логином и паролем."""
        response = requests.post(self.url, json={"email": login, "password": auth_db[login]})
        assert response.status_code == 200
        body = response.json()
        assert "token" in body, "В теле ответа отсутствует 'token'"

    @pytest.mark.parametrize("password", ["", " ", "cityslick"])
    @pytest.mark.parametrize("login", auth_db.keys())
    def test_auth_with_invalid_password(self, login, password):
        """Авторизация с невалидным паролем."""
        response = requests.post(self.url, json={"email": login, "password": password})
        assert response.status_code == 400

    @pytest.mark.parametrize("login", ["", " ", "eve.holt"])
    def test_auth_with_invalid_login(self, login):
        """Авторизация с невалидным логином."""
        response = requests.post(self.url, json={"email": login, "password": "password"})
        assert response.status_code == 400

    @pytest.mark.parametrize("auth_data", [{"email": "", "password": ""}, {"email": " ", "password": " "}])
    def test_auth_with_invalid_login_password(self, auth_data):
        """Авторизация с пустыми логином/паролем."""
        response = requests.post(self.url, json=auth_data)
        assert response.status_code == 400

    @pytest.mark.parametrize("auth_data", [{"email": "1@1.ru"}, {"password": "password"}])
    def test_auth_with_invalid_data(self, auth_data):
        """Авторизация с невалидной структурой запроса - отсутствует логин или пароль."""
        response = requests.post(self.url, json=auth_data)
        assert response.status_code == 422

